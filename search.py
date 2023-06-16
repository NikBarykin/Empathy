from agent import Agent


def search(agent: Agent, agents_pool):
    scores = dict()
    candidates = []

    for target_agent in agents_pool:
        score = agent.rate(target_agent)
        if score <= 0:
            continue

        scores[target_agent.user_id] = score
        candidates.append(target_agent)

    candidates.sort(key=lambda agent: scores[agent.user_id], reverse=True)

    return candidates
