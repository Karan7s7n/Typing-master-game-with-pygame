# **Typing Master – A Fast-Paced Typing Game in Python (Pygame)**  

## **Overview**  
**Typing Master** is a fun and challenging typing speed game built using **Python and Pygame**. The goal is to type words as they appear on the screen before they disappear. The game includes **multiple levels**, background music, sound effects, and a scoring system. It also maintains the highest score using a local file.  

## **Features**  
✅ **Word Typing Challenge** – Type falling words before they reach the left edge of the screen.  
✅ **Multiple Levels** – The game increases difficulty with each level.  
✅ **Dynamic Word Selection** – Words are chosen from the **NLTK corpus**, sorted by length.  
✅ **Sound Effects & Background Music** – Enhances the gaming experience.  
✅ **High Score System** – Saves the highest score in a file (`high.txt`).  
✅ **Pause & Resume Feature** – Allows pausing and resuming the game.  
✅ **Interactive UI with Buttons** – Implemented using Pygame’s graphics system.  

---

## **Gameplay**  
🎯 **Objective:** Type the words correctly before they disappear off the screen.  
🎮 **Controls:**  
- **Type letters** on the keyboard to complete the word.  
- **Backspace** to delete characters.  
- **Enter/Spacebar** to submit the typed word.  
- **Esc** to pause/unpause the game.  
- **Mouse Clicks** to interact with the UI buttons.  

🚀 **Scoring System:**  
- Each correct word increases the score based on word length and speed.  
- If a word is not typed in time, **lives decrease**.  
- If lives reach **zero**, the game resets.  

## **Code Structure**  
📂 **Project Structure:**  
```
/typing-master
│── typemaster.py         # Main game logic
│── high.txt              # Stores the highest score
│── digital-7.ttf         # Font file for game text
│── music.mp3             # Background music
│── click.mp3             # Typing sound effect
│── swosh.mp3             # Correct word sound
│── error.mp3             # Wrong word sound
```

### **Key Components in `typemaster.py`**
📌 **Word Selection from NLTK:**  
- Loads a word list from the **NLTK corpus** and sorts words by length.  
- Different levels control word length selection.  

📌 **Game UI:**  
- Uses **Pygame’s `Surface` and `draw` methods** to render buttons and text.  
- Implements a **pause menu** with clickable buttons.  

📌 **Game Loop & Logic:**  
- Continuously spawns words with random positions and speeds.  
- Tracks user input and updates score accordingly.  
- Stores the **highest score in `high.txt`** for persistence.  

📌 **Images & video:**
<img width="801" height="629" alt="tm 1" src="https://github.com/user-attachments/assets/b96eda07-2842-4f21-abb5-77fa4bf8e3e6" />
<img width="801" height="629" alt="tm 2" src="https://github.com/user-attachments/assets/3dab27a3-eca7-4936-bbf8-db5ec7d014f7" />


