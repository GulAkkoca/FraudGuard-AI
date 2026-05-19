from services.scrapers.trendyol_scraper import (
    build_review_urls,
    extract_category_from_html,
    extract_average_rating,
    extract_price_from_html,
    extract_product_content_id,
    extract_reviews_from_html,
    extract_seller_rating_from_html,
    extract_seller_verified_from_html,
    normalize_descriptions,
    normalize_reviews,
)


def test_extract_product_content_id_from_trendyol_url():
    url = "https://www.trendyol.com/brand/product-name-p-951534808"

    assert extract_product_content_id(url) == "951534808"


def test_extract_product_content_id_from_review_read_api_url():
    url = (
        "https://apigw.trendyol.com/discovery-storefront-trproductgw-service/"
        "api/review-read/product-reviews/detailed?contentId=1078142016&page=0&pageSize=20&channelId=1"
    )

    assert extract_product_content_id(url) == "1078142016"


def test_build_review_urls_prefers_current_apigw_review_read_endpoint():
    urls = build_review_urls("1016742922")

    assert urls[0] == (
        "https://apigw.trendyol.com/discovery-storefront-trproductgw-service/"
        "api/review-read/product-reviews/detailed?contentId=1016742922"
        "&page=0&pageSize=20&channelId=1"
    )


def test_extract_price_from_embedded_document_json():
    html = """
    {
      "price": {
        "currency": "TRY",
        "discountedPrice": {"value": 303.38, "text": "303,38 TL"},
        "sellingPrice": {"value": 303.38, "text": "303,38 TL"},
        "originalPrice": {"value": 399.99, "text": "399,99 TL"}
      }
    }
    """

    price = extract_price_from_html(html)

    assert price["current_price"] == 303.38
    assert price["selling_price"] == 303.38
    assert price["original_price"] == 399.99
    assert price["currency"] == "TRY"


def test_extract_price_prefers_winner_variant_over_other_merchants():
    html = """
    <script>
      window["__envoy__SHARED_PROPS"] = {
        "product": {
          "merchantListing": {
            "otherMerchants": [
              {
                "price": {
                  "currency": "TRY",
                  "discountedPrice": {"value": 383, "text": "383 TL"},
                  "sellingPrice": {"value": 383, "text": "383 TL"},
                  "originalPrice": {"value": 383, "text": "383 TL"}
                }
              }
            ],
            "winnerVariant": {
              "price": {
                "currency": "TRY",
                "discountedPrice": {"value": 359.4, "text": "359,40 TL"},
                "sellingPrice": {"value": 359.4, "text": "359,40 TL"},
                "originalPrice": {"value": 359.4, "text": "359,40 TL"},
                "tyPlusCouponApplicablePrice": {"value": 314.21, "text": "314,21 TL"}
              }
            }
          }
        }
      };
    </script>
    """

    price = extract_price_from_html(html)

    assert price["current_price"] == 314.21
    assert price["selling_price"] == 359.4
    assert price["original_price"] == 359.4
    assert price["discounted_price"] == 359.4
    assert price["basket_price"] == 314.21


def test_extract_product_metadata_from_document_response_state():
    html = """
    <script>
      window["__envoy__SHARED_PROPS"] = {
        "product": {
          "category": {"id": 650, "name": "Maskara"},
          "merchantListing": {
            "merchant": {
              "name": "CosmeticBox",
              "sellerScore": {"value": 9.2, "color": "#049B24"},
              "merchantBadges": [
                {
                  "webImageUrl": "https://cdn.dsmcdn.com/mobile/pdp/Seller_badge/yetkilisatici.svg",
                  "type": "BADGE"
                }
              ]
            }
          }
        }
      };
    </script>
    """

    assert extract_category_from_html(html) == "Maskara"
    assert extract_seller_rating_from_html(html) == 9.2
    assert extract_seller_verified_from_html(html) is True


def test_extract_seller_verified_false_when_badges_have_no_verified_signal():
    html = """
    <script>
      window["__envoy__SHARED_PROPS"] = {
        "product": {
          "merchantListing": {
            "merchant": {
              "merchantBadges": [
                {"webImageUrl": "https://cdn.dsmcdn.com/mobile/pdp/other.svg", "type": "BADGE"}
              ]
            }
          }
        }
      };
    </script>
    """

    assert extract_seller_verified_from_html(html) is False


def test_extract_reviews_from_json_ld_document_response():
    html = """
    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "Product",
        "review": [
          {
            "@type": "Review",
            "datePublished": "2026-01-14",
            "reviewBody": "Cok guzel urun.",
            "reviewRating": {"@type": "Rating", "ratingValue": 5}
          }
        ]
      }
    </script>
    """

    reviews = extract_reviews_from_html(html)

    assert len(reviews) == 1
    assert reviews[0].rating == 5
    assert reviews[0].text == "Cok guzel urun."
    assert reviews[0].date == "2026-01-14"


def test_normalize_reviews_from_trendyol_response():
    response = {
        "result": {
            "summary": {"averageRating": 4.2},
            "reviews": [
                {
                    "rate": 5,
                    "comment": "Urun guzel.",
                    "createdAt": "2026-05-16",
                    "likesCount": 3,
                    "seller": {"name": "Calliel"},
                }
            ],
        }
    }

    reviews = normalize_reviews(response)

    assert extract_average_rating(response) == 4.2
    assert reviews[0].rating == 5
    assert reviews[0].text == "Urun guzel."
    assert reviews[0].seller_name == "Calliel"


def test_normalize_reviews_from_current_apigw_review_read_response():
    response = {
        "result": {
            "reviews": [
                {
                    "rate": 5,
                    "comment": "Bayildim, tek katta bile fark gorunuyor.",
                    "createdAt": 1768397108743,
                    "likesCount": 5,
                    "seller": {"id": 1047362, "name": "CosmeticBox"},
                }
            ]
        }
    }

    reviews = normalize_reviews(response)

    assert len(reviews) == 1
    assert reviews[0].rating == 5
    assert reviews[0].text == "Bayildim, tek katta bile fark gorunuyor."
    assert reviews[0].date == "2026-01-14"
    assert reviews[0].likes_count == 5
    assert reviews[0].seller_name == "CosmeticBox"


def test_normalize_descriptions_extracts_seller_name():
    response = {
        "result": {
            "descriptions": [
                {
                    "text": "Tum cilt tiplerine uygun gunes kremidir.",
                    "textComponents": {
                        "pre": "Bu urun",
                        "mid": "Calliel",
                        "post": "tarafindan gonderilecektir.",
                    },
                }
            ]
        }
    }

    data = normalize_descriptions(response)

    assert data["seller_name"] == "Calliel"
    assert "gunes kremidir" in data["product_description"]
