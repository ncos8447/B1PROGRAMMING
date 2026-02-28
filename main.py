#Music library manager
#Step 1

songs = []
genre_count = {}

print("Welcome to Music Library Manager!")

#Step 2-3

for i in range(1, 6):
    print(f"\nEnter song {i}:")
    title = str(input(" Song name: "))
    genre = str(input(" Genre: "))

    info = (title, genre)
    songs.append(info)

    genre_count[genre] = genre_count.get(genre, 0) + 1

#Step 4

print("\n=== YOUR MUSIC LIBRARY ===")

for index, (title, genre) in enumerate(songs, 1):
    print(f"{index}. {title} ({genre})")

print("\n=== GENRE STATISTICS ===")

for genre, count in genre_count.items:
    print(f"{genre}: {count} songs")

most_popular = max(genre_count, key=genre_count.get)
print(f"\nMost popular genre: {most_popular}")