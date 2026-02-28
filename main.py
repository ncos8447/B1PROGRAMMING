#student grade analyzer

#part a
student_records = []
stats = {}

for i in range(1, 7):
    name = str(input(f"Student's name: "))

    #score validation
    while True:
        try:
            score = float(input("  Score (0-100): "))
            if 0 <= score <= 100:
                break
            else:
                print("    Score must be between 0 and 100.")
        except ValueError:
            print("    Please enter a valid number.")
    student_records.append((name, score))

#stats

scores = [score for name, score in student_records]

stats["highest"] = max(scores)
stats["lowest"] = min(scores)
stats["average"] = sum(scores) / len(scores)

unique_scores = set(scores)

grade_distribution = {}
for score in scores:
    grade_distribution[str(score)] = grade_distribution.get(str(score), 0) + 1

#display results

print("\n=== STUDENT RECORDS ===")

for i in range(1, 7):
    print(f"{i}. {student_records[i-1][0]}: {student_records[i-1][1]}")

print("\n=== STATISTICS ===")

print(f"Highest Score: {stats["highest"]}")
print(f"Lowest Score: {stats["lowest"]}")
print(f"Average Score: {stats["average"]:.2f}")

print("\n=== UNIQUE SCORES ===")
print(unique_scores)
print(f"Total unique scores: {len(unique_scores)}")

print("\n=== GRADE DISTRIBUTION ===")
for score, number in sorted(grade_distribution.items(), reverse=True):
    if number == 1:
        print(f"Score {score}: {number} student")
    else:
        print(f"Score {score}: {number} students")