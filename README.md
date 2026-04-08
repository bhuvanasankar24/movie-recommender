# 🎬 Movie Recommender System

A smart Movie Recommendation System built using **Machine Learning (Content-Based Filtering)** that suggests movies based on genre, cast, and similarity.

---

## 🚀 Live Demo

👉 ??? *(add your deployed link here)*

---

## 📌 Features

* 🔍 Search and select any movie
* 🎯 Genre-aware recommendations (high accuracy)
* 🧠 Content-based filtering using cosine similarity
* 🎥 Displays movie posters dynamically
* ⚡ Fast and responsive Streamlit UI
* 🔄 Adaptive filtering (strict → relaxed for better results)

---

## 🧠 How It Works

This system uses:

### 🔹 Content-Based Filtering

* Recommends movies similar to the selected movie

### 🔹 Feature Engineering

* Genres (high priority)
* Keywords
* Cast
* Crew (Director)

### 🔹 Vectorization

* TF-IDF Vectorizer converts text → numerical vectors

### 🔹 Similarity Calculation

* Cosine Similarity measures closeness between movies

### 🔹 Smart Filtering

* First filters by strong genre match
* Then ranks using similarity score

---

## 🛠️ Tech Stack

* Python 
* Pandas & NumPy
* Scikit-learn
* Streamlit
* OMDb API (for posters)

---

## 📂 Project Structure

```
movie-recommender/
│
├── app.py              # Streamlit UI
├── model.py            # Data preprocessing & model building
├── requirements.txt    # Dependencies
```

---

## ⚙️ Installation & Run Locally

```bash
git clone https://github.com/bhuvanaasankar24/movie-recommender.git
cd movie-recommender

pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Deployment

Deployed using **Streamlit Cloud**:

1. Push code to GitHub
2. Connect repo to Streamlit Cloud
3. Deploy `app.py`

---

## 💡 Key Improvements Implemented

* ✔ Removed noisy overview text
* ✔ Increased weight for genres
* ✔ Hybrid recommendation (Genre + Similarity)
* ✔ Adaptive filtering (ensures results always appear)
* ✔ Error handling & fallback mechanisms

---

## 🎯 Future Enhancements

* ⭐ Add movie ratings & overview
* 🎨 Netflix-style UI design
* 🔍 Real-time search bar
* 🤖 Collaborative filtering
* 🌍 Multi-language support

---

## 🙌 Acknowledgements

* TMDB Dataset (Kaggle)
* OMDb API for movie posters

---

## 👩‍💻 Author

**Bhuvana Sankar**
Bhuvaneshwari S

LinkedIn - www.linkedin.com/in/bhuvana-sankar,

Mail - bhuvanaasankar241@gmail.com

---
This project is for educational purposes. You can use and modify it freely.
---
## ⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!
