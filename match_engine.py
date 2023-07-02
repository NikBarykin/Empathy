from agent import Agent


def find_match(agent: Agent, agents):
    rate = lambda obj: rate_match(agent, obj)

    best_match = max(
            agents,
            key=rate)

    return (best_match if rate(best_match) > 0
            else None)

def rate_match(subj: Agent, obj: Agent) -> float:
    if (obj.user_id == subj.user_id
        or obj.gender == subj.gender
        or obj.user_id in subj.disliked_ids
        or obj.user_id in subj.liked_ids
        or obj.age > subj.max_preferred_age
        or obj.age < subj.min_preferred_age
        ):
        return -1 # we don't want to date oursubj or someone with the same gender

    return 1
