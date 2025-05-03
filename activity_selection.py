
def select_activities(tasks):
    tasks = [(name, int(start), int(end)) for name, start, end in tasks]
    
    sorted_tasks = sorted(tasks, key=lambda x: x[2])
    
    result = []
    last_end = -1
    
    for name, start, end in sorted_tasks:
        if start >= last_end:
            result.append((name, start, end))
            last_end = end
            
    return result
