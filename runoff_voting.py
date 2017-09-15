def runoff(voters):

    #This function takes an array of votes and finds the winning candidate
    #according to the runoff voting mechanism. Runoff voting works as follows:
    #Each voter ranks all candidates in order of preference. Initially all
    #voters' first preferences are compared. If a candidate is ranked as first
    #for more than half the voters, that candidate wins. If not, the candidate
    #who recieved the least amount of first preference votes is removed. Then
    #the process is repeated. If more than one candidate draws for last place
    #both are removed.
    #An example of an array with 3 voters and 4 candidates is:
    #[[A,C,D,B], [A,B,D,C], [D,B,A,C]] (in this case, A wins)
    
    if not voters[0]:
        return None
        
    candidate_vote_cnt = {candidate: 0 for candidate in voters[0]}
    first_votes = [candidate[0] for candidate in voters]
    
    
    vote_count = 0
    for candidate in voters[0]:
        vote_count = first_votes.count(candidate)
        if vote_count / len(voters) > 0.5:
            return candidate
        else:
            candidate_vote_cnt[candidate] = vote_count
    
    
    min_votes = min(candidate_vote_cnt.values())
    for candidate, votes in candidate_vote_cnt.iteritems():
        if votes == min_votes:
            for i in voters:
                try:
                    i.remove(candidate)
                except ValueError:
                    pass
            
    return runoff(voters)
