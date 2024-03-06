from utils.db_api.database import conn,cur




cur.execute("""CREATE TABLE IF NOT EXISTS sender_handlers(
    id INT DEFAULT 0,
    text TEXT DEFAULT NULL,
    video_id TEXT DEFAULT NULL,
    photo_id TEXT DEFAULT NULL
    )
""")


def refresh_db():
    if get_sender_data() == None:
        cur.execute("INSERT INTO sender_handlers VALUES(0,NULL,NULL,NULL)")
    cur.execute("UPDATE sender_handlers SET text = NULL WHERE id = 0")
    conn.commit()
    cur.execute("UPDATE sender_handlers SET video_id = NULL WHERE id = 0")
    conn.commit()
    cur.execute("UPDATE sender_handlers SET photo_id = NULL WHERE id = 0")
    conn.commit()

def set_text(text):
    cur.execute("UPDATE sender_handlers SET text = ? WHERE id = 0",(text,))
    conn.commit()

def set_videoId(videoId):
    cur.execute("UPDATE sender_handlers SET video_id = ? WHERE id = 0",(videoId,))
    conn.commit()

def set_photoId(photoId):
    cur.execute("UPDATE sender_handlers SET photo_id = ? WHERE id = 0",(photoId,))
    conn.commit()

def get_sender_data():
    crtj = cur.execute("SELECT * FROM sender_handlers WHERE id = 0").fetchone()
    if crtj == None:
        cur.execute("INSERT INTO sender_handlers VALUES(0,NULL,NULL,NULL)")
        conn.commit()
        crtj = cur.execute("SELECT * FROM sender_handlers WHERE id = 0").fetchone()
    id = crtj[0]
    text = crtj[1]
    video_id = crtj[2]
    photo_id = crtj[3]
    d = {'id':id,'text':text,'video_id':video_id,'photo_id':photo_id}
    return d