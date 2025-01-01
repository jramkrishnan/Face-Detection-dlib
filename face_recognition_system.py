# face_recognition_system.py
import face_recognition
import cv2
import numpy as np
import os
from pathlib import Path
import sqlite3
from datetime import datetime
import threading
from contextlib import contextmanager

class FaceRecognitionSystem:
    def __init__(self, known_faces_dir="known_faces"):
        self.known_faces_dir = known_faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()
        self.init_database()
        self._lock = threading.Lock()
        
    def init_database(self):
        """Initialize SQLite database with proper schema"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            # Create attendance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_name TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date DATE DEFAULT (date('now','localtime'))
                )
            ''')
            conn.commit()
    
    @contextmanager
    def get_db_connection(self):
        """Thread-safe database connection context manager"""
        conn = sqlite3.connect('face_recognition.db')
        try:
            yield conn
        finally:
            conn.close()
    
    def load_known_faces(self):
        """Load all images from the known_faces directory"""
        Path(self.known_faces_dir).mkdir(exist_ok=True)
        
        for image_file in os.listdir(self.known_faces_dir):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                name = os.path.splitext(image_file)[0]
                image_path = os.path.join(self.known_faces_dir, image_file)
                try:
                    face_image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(face_image)
                    
                    if face_encodings:
                        self.known_face_encodings.append(face_encodings[0])
                        self.known_face_names.append(name)
                        print(f"Loaded face: {name}")
                    else:
                        print(f"No face found in image: {image_file}")
                except Exception as e:
                    print(f"Error loading {image_file}: {str(e)}")
    
    def record_attendance(self, name):
        """Record attendance in a thread-safe manner"""
        with self._lock:
            try:
                with self.get_db_connection() as conn:
                    cursor = conn.cursor()
                    # Check if person already has attendance for today
                    cursor.execute('''
                        SELECT id FROM attendance 
                        WHERE person_name = ? 
                        AND date = date('now', 'localtime')
                    ''', (name,))
                    
                    if not cursor.fetchone():
                        cursor.execute('''
                            INSERT INTO attendance (person_name) 
                            VALUES (?)
                        ''', (name,))
                        conn.commit()
            except Exception as e:
                print(f"Error recording attendance: {str(e)}")
    
    def get_attendance_report(self):
        """Get attendance report for today"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT person_name, time(timestamp) as time
                    FROM attendance
                    WHERE date = date('now', 'localtime')
                    ORDER BY timestamp
                ''')
                return cursor.fetchall()
        except Exception as e:
            print(f"Error getting attendance report: {str(e)}")
            return []
    
    def process_frame(self, frame):
        """Process a single frame and return the frame and any recognized names"""
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        recognized_names = []
        
        try:
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    
                    if True in matches:
                        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                            recognized_names.append(name)
                            self.record_attendance(name)
                    
                    # Scale back up face locations
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    
                    # Draw face box and name
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
        
        return frame, recognized_names
