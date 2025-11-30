import csv
from db_config import get_connection

CSV_PATH = "Most Streamed Spotify Songs 2024_clean.csv"

def to_int(value):
    if not value or value.strip() == "":
        return 0
    value = value.replace(",", "")
    return int(value)

def import_csv():
    conn = get_connection()
    cursor = conn.cursor()

    with open(CSV_PATH, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        rows = 0
        for row in reader:
            sql = """
            INSERT INTO spotify_songs (
                track,
                artist,
                release_date,
                spotify_streams,
                spotify_popularity,
                youtube_views,
                explicit_track
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                row["Track"],
                row["Artist"],
                row["Release Date"],
                to_int(row["Spotify Streams"]),
                to_int(row["Spotify Popularity"]),
                to_int(row["YouTube Views"]),
                row["Explicit Track"],
            )

            cursor.execute(sql, values)
            rows += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Import CSV selesai. Total baris masuk: {rows}")

if __name__ == "__main__":
    import_csv()
