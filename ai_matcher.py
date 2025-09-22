def rank_jobs(jobs, skills, role):
    # Very simple keyword matching for now
    keywords = (skills + " " + role).lower().split()
    scored_jobs = []

    for job in jobs:
        score = sum(1 for kw in keywords if kw in job["title"].lower())
        scored_jobs.append((score, job))

    # Sort jobs by score, highest first
    scored_jobs.sort(reverse=True, key=lambda x: x[0])
    return [job for _, job in scored_jobs[:5]]
