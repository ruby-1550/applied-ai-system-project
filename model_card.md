# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeMatch Mini 1.0

---

## 2. Intended Use

This model suggests 5 songs from a small class dataset.  
It assumes a single user has clear preferences for genre, mood, and vibe numbers.  
It is for classroom exploration, not real users.

---

## 3. Goal / Task

The goal is to predict which songs a user might like next.  
It does this by matching a user profile to song features.  
It is a simple content-based recommender.

---

## 4. Data Used

The dataset has 18 songs in `data/songs.csv`.  
Each song has genre, mood, energy, tempo, valence, danceability, and acousticness.  
I added extra genres like metal, classical, hip hop, and indie folk.  
The dataset is small and does not cover all tastes.

---

## 5. Algorithm Summary

The model gives points for exact matches in genre and mood.  
It adds more points when numeric features are close to the user's targets.  
Energy has the strongest weight, so high-energy matches rise quickly.  
Songs are sorted by total score and the top K are returned.

---

## 6. Observed Behavior / Biases

High-energy songs often win even if mood does not match.  
Smaller genres can lose out because there are fewer examples.  
The scoring treats each feature separately, so mixed feelings (high energy but sad) can look odd.  
This can create a mild filter bubble around the strongest feature.

---

## 7. Evaluation Process

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and Conflicting High-Energy Sad.  
I checked the top five songs and read the reasons for each score.  
I ran an experiment that doubled the energy weight and halved the genre points.  
The results became even more energy-heavy, which showed the model is sensitive to weights.

---

## 8. Intended Use and Non-Intended Use

Intended use: classroom demos and learning how scoring works.  
Non-intended use: real music recommendations, user profiling, or any high-stakes decisions.  
The dataset and logic are too small and too simple for real use.

---

## 9. Ideas for Improvement

Add more songs and balance genres and moods.  
Add a diversity rule so the top results are not all the same style.  
Use a better distance function for tempo and mood together.

---

## 10. Personal Reflection

My biggest learning moment was seeing how weight choices can change everything.  
AI tools helped me draft profiles and reason about scoring, but I still had to verify the math.  
It surprised me how a simple score can still feel like a real recommendation.  
Next I would try a hybrid method that mixes user behavior with these song features.
