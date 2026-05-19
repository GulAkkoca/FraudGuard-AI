import { Activity } from "lucide-react";

export default function AgentTimeline({ agents = [], strongestAgent }) {
  return (
    <section className="surface">
      <div className="section-title">
        <Activity size={19} />
        <h2>Agent Timeline</h2>
      </div>
      <div className="timeline">
        {agents.map((agent) => (
          <article key={agent.agent_name} className={agent.agent_name === strongestAgent?.agent_name ? "focus" : ""}>
            <div>
              <strong>{agent.agent_name}</strong>
              <span>{Math.round(agent.risk_score)}/100</span>
            </div>
            <meter min="0" max="100" value={agent.risk_score} />
          </article>
        ))}
      </div>
    </section>
  );
}

