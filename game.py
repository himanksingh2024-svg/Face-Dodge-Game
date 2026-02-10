import cv2
import mediapipe as mp
import random
import numpy as np

# --- GAME SETTINGS (Now HD!) ---
WIDTH, HEIGHT = 1280, 720  # Increased to HD resolution
PLAYER_WIDTH = 100         # Made player slightly bigger
ENEMY_SIZE = 50
ENEMY_SPEED = 10 

# --- SETUP CAMERA & FACE DETECTOR ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)
# Request HD quality from webcam
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# --- FULLSCREEN SETUP (NEW!) ---
cv2.namedWindow('Head Dodge', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Head Dodge', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# --- VARIABLES ---
player_x = WIDTH // 2
enemies = [] 
score = 0
game_over = False

while True:
    ret, frame = cap.read()
    if not ret: break
    
    # Resize frame to ensure it fills the HD settings
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    
    # Flip frame (mirror effect)
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect Face
    results = face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        nose = results.multi_face_landmarks[0].landmark[1]
        player_x = int(nose.x * WIDTH) - (PLAYER_WIDTH // 2)

    # Game Logic
    if not game_over:
        # Spawn Enemies
        if random.random() < 0.05:
            enemies.append([random.randint(0, WIDTH-ENEMY_SIZE), 0])

        # Move & Draw Enemies
        for enemy in enemies:
            enemy[1] += ENEMY_SPEED
            cv2.rectangle(frame, (enemy[0], enemy[1]), (enemy[0]+ENEMY_SIZE, enemy[1]+ENEMY_SIZE), (0,0,255), -1)
            
            # Collision Check
            if (enemy[1] + ENEMY_SIZE >= HEIGHT - 50 and 
                enemy[0] + ENEMY_SIZE >= player_x and 
                enemy[0] <= player_x + PLAYER_WIDTH):
                game_over = True

        enemies = [e for e in enemies if e[1] < HEIGHT]
        score += 1

        # Draw Player
        cv2.rectangle(frame, (player_x, HEIGHT-50), (player_x+PLAYER_WIDTH, HEIGHT-50+20), (255,0,0), -1)
        cv2.putText(frame, f"Score: {score}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3)
    
    else:
        cv2.putText(frame, "GAME OVER", (WIDTH//2 - 200, HEIGHT//2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
        cv2.putText(frame, "Press 'R' to Restart", (WIDTH//2 - 180, HEIGHT//2 + 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        if cv2.waitKey(1) & 0xFF == ord('r'):
            game_over = False
            enemies = []
            score = 0

    cv2.imshow('Head Dodge', frame)
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()