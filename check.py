import json
with open('correct_answer.json', 'r') as correct, open('my_results.json', 'r') as results:
    count = 1
    for liner, linec in zip(results, correct):
        dictr = json.loads(liner)
        dictc = json.loads(linec)
        if dictc == dictr or (dictr['status'] == 'ERROR' and dictc['status'] == 'ERROR'):
            print("{}: OK".format(count))
        elif dictr['status'] == 'NOT IMPLEMENTED':
            print('{}: NOT IMPLEMENTED'.format(count))
        else:
            print("{}: WRONG ANSWER".format(count))
            print("Expected: {}".format(dictc))
            print("Given: {}".format(dictr))
        count += 1
