import { CheckCircle2, CircleDashed } from "lucide-react";

export default function LoadingSteps({ steps, activeStep, loading }) {
  return (
    <ol className="loading-steps">
      {steps.map((step, index) => {
        const done = loading && index <= activeStep;
        return (
          <li key={step} className={done ? "done" : ""}>
            {done ? <CheckCircle2 size={17} /> : <CircleDashed size={17} />}
            <span>{step}</span>
          </li>
        );
      })}
    </ol>
  );
}

