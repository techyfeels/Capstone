from db_config import get_connection
from prettytable import PrettyTable
import matplotlib.pyplot as plt


def read_table(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        track,
        artist,
        release_date,
        spotify_streams,
        spotify_popularity,
        youtube_views,
        explicit_track
    FROM spotify_songs
    ORDER BY spotify_streams DESC
    LIMIT %s;
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = [
        "Track", 
        "Artist", 
        "Release Date", 
        "Spotify Streams", 
        "Spotify Popularity", 
        "YouTube Views", 
        "Explicit Track"
    ]
    
    for row in rows:
        table.add_row(row)

    print("\n=== DATA SPOTIFY SONGS (TOP {}) ===".format(limit))
    print(table)

    cursor.close()
    conn.close()


def show_statistic():
    conn = get_connection()
    cursor = conn.cursor()

    #1) Aggregated stats: total, avarage, sum
    cursor.execute("""
        SELECT 
            COUNT(*),
            AVG(spotify_streams),
            AVG(spotify_popularity),
            SUM(youtube_views)           
        FROM spotify_songs;
    """)
    total_songs, avg_streams, avg_popularity, total_youtube = cursor.fetchone()

    #2) track with highest streams
    cursor.execute("""
        SELECT track, artist, spotify_streams
        FROM spotify_songs
        ORDER BY spotify_streams DESC
        LIMIT 1;
    """)
    max_track, max_artist, max_streams = cursor.fetchone()

    #3) track with lowest streams
    cursor.execute("""
        SELECT track, artist, spotify_streams
        FROM spotify_songs
        ORDER BY spotify_streams ASC
        LIMIT 1;
    """)
    min_track, min_artist, min_streams = cursor.fetchone()

    # Handle none
    avg_streams_str = f"{int(avg_streams):,}" if avg_streams is not None else "N/A"
    avg_popularity_str = f"{float(avg_popularity):.2f}" if avg_popularity is not None else "N/A"
    total_youtube_str = f"{int(total_youtube):,}" if total_youtube is not None else "N/A"

    print("\n=== STATISTICS ===")
    print(f"Total Songs: {total_songs:,}")
    print(f"Average Streams: {avg_streams_str}")
    print(f"Average Popularity: {avg_popularity_str}")
    print(f"Total YouTube Views: {total_youtube_str}")
    print(f"Track with Highest Streams: {max_track} - {max_artist}({max_streams:,} streams)")
    print(f"Track with Lowest Streams: {min_track} - {min_artist}({min_streams:,} streams)")

    cursor.close()
    conn.close()

input("\nPress Enter to continue...")

def show_visualization():
   
    #1) Histogram Top 200
    conn1 = get_connection()
    cursor1 = conn1.cursor()
    
    cursor1.execute("""
        SELECT spotify_streams
        from spotify_songs;
        ORDER BY spotify_streams DESC;
        LIMIT 200;
    """) 
    rows = cursor1.fetchall()
    
    cursor1.close()
    conn1.close()

    streams = [r[0] for r in rows if r[0] is not None]

    if streams:
        plt.figure()
        plt.hist(streams, bins=20)
        plt.title("Histogram of Spotify Streams (Top 200)")
        plt.xlabel("Spotify Streams")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()
    else:
        print("No data available for visualization.")

    #2) bar chart : top 10 artist
    conn2 = get_connection()
    cursor2 = conn2.cursor()
    
    cursor2.execute("""
        SELECT artist, SUM(spotify_streams) as total_streams
        FROM spotify_songs
        GROUP BY artist
        ORDER BY total_streams DESC
        LIMIT 10;
    """)
    rows = cursor2.fetchall()
    
    cursor2.close()
    conn2.close()

    artists = [r[0] for r in rows]
    artist_streams = [r[1] for r in rows] 

    if artists and artist_streams:
        plt.figure()    
        plt.bar(range(len(artists)), artist_streams)
        plt.xticks(range(len(artists)), artists, rotation=45, ha='right')
        plt.xlabel("Artist")
        plt.ylabel("Total Streams")
        plt.tight_layout()
        plt.show()
    else:
        print("No data available for visualization.") 

    input("\nPress Enter to continue...")

def add_song():
    print("\n=== ADD NEW SONG ===")

    #ambil input user
    track = input("Track name: ").strip()
    artist = input("Artist name: ").strip()
    release_date = input("Release date (YYYY-MM-DD): ").strip()

    try:
        spotify_streams = int(input("Spotify streams (angka): "))
    except:
        print("Invalid input. stream harus angka Please try again.")
        return
    
    try:
        spotify_popularity = int(input("Spotify popularity (0-100): "))
    except:
        print("Invalid input. Popularity harus angka Please try again.")
        return

    try:
        youtube_views = int(input("YouTube views (angka): "))
    except:
        print("Invalid input. Views harus angka Please try again.")
        return

    explicit = input("Explicit? (0 = no, 1 = yes): ").strip()
    if explicit not in ("0", "1"):
        print("Explicit harus 0 atau 1. Please try again.")
        return
    
    #konfirmasi sebelum insert
    print("\nData yang akan disimpan:") 
    print(f"Track: {track}")        
    print(f"Artist: {artist}")
    print(f"Date: {release_date}")
    print(f"Streams: {spotify_streams}")
    print(f"Popularity: {spotify_popularity}")
    print(f"YouTube Views: {youtube_views}")
    print(f"Explicit: {explicit}")

    confirm = input("\nSimpan data ini? (y/n): ").lower()
    if confirm != "y":
        print("Dibatalkan.")
        return


    #insert data ke database
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO spotify_songs (
    track, artist, release_date, spotify_streams, 
    spotify_popularity, youtube_views, explicit_track
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    data = (
    track, 
    artist, 
    release_date, 
    spotify_streams, 
    spotify_popularity, 
    youtube_views, 
    explicit
    )


    cursor.execute(insert_query,data)
    conn.commit()

    cursor.close()
    conn.close()


    print("\nSong insterted successfully.")
    input("\nPress Enter to continue...")


def main_menu():
    while True:
        print("\n=== SPOTIFY APP (CAPSTONE MOD 1) ===")
        print("1. Lihat data (top 20)")
        print("2. Exit")
        print("3. Lihat Statistik")
        print("4. Visualisasi")
        print("5. Upload Data Song")


        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            read_table()
        elif choice == "2":
            print("Goodbye!")
            break
        elif choice == "3":
            show_statistic()
        elif choice == "4":
            show_visualization()
        elif choice == "5":
            add_song()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
