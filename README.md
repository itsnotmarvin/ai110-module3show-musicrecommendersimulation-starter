# 🎵 Music Recommender Simulation

## Project Summary

This project is a small, explainable music recommender. It compares the features of each song in a ten-song catalog to a listener's taste profile and returns the best matches. Instead of making a hidden prediction, it also explains why each song received its recommendation, such as a genre match, mood match, similar energy level, or acousticness preference.

The project includes the same recommendation idea in two forms: an object-oriented `Recommender` class using `Song` and `UserProfile` objects, and a functional version using dictionaries. This made it easier to see that the important part of a recommender is the scoring rule, not just the programming style.

## How The System Works

Each song has a genre, mood, energy level, tempo, valence, danceability, and acousticness. The current scoring rule uses genre, mood, energy, and acousticness because those are the preferences stored in the user profile.

The user profile stores a favorite genre, favorite mood, target energy level from 0 to 1, and whether the listener likes more acoustic music. Every song starts with a score of zero. The recommender then adds:

- 3 points for a matching genre
- 2.5 points for a matching mood
- up to 2.5 points for an energy level close to the target
- 1 point when the song's acousticness matches the user's preference

The songs are sorted from highest to lowest score. Ties are sorted by title so that the results stay consistent. Each recommendation includes the score and the matching features that contributed to it.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Run the app from this project folder:

   ```bash
   python3 -m src.main
   ```

### Running Tests

Run the tests with:

```bash
python3 -m pytest -q
```

## Sample Recommendation Output

Using the starter profile (`pop`, `happy`, target energy `0.8`, and a preference for less acoustic music), the program produces:

```text
Top recommendations:

Sunrise City - Score: 8.95
Because: Recommended because it matches your favorite genre (pop), it matches your preferred mood (happy), its energy is close to your target, it fits your preference for less acoustic music.

Gym Hero - Score: 6.17
Because: Recommended because it matches your favorite genre (pop), its energy is close to your target, it fits your preference for less acoustic music.

Rooftop Lights - Score: 5.90
Because: Recommended because it matches your preferred mood (happy), its energy is close to your target, it fits your preference for less acoustic music.
```

## Experiments I Tried

I tested the starter pop/happy/high-energy profile and checked whether energetic pop songs reached the top. `Sunrise City` ranked first because it matches both genre and mood and is extremely close to the requested energy. `Gym Hero` ranked next because it matches the genre and energy even though its mood is `intense` instead of `happy`.

I also considered the effect of the weights. Genre has the largest weight because it is usually a strong signal of taste in this small catalog. Mood and energy can still move a song upward, so a happy indie-pop track such as `Rooftop Lights` can rank above songs that only happen to have similar energy. The acousticness point is deliberately smaller so that it refines a recommendation instead of overpowering genre and mood.

## Limitations and Risks

This system only has ten songs, so it cannot represent the range of real musical taste. It ignores lyrics, language, listening history, artists, novelty, context, and whether a listener wants variety. It also treats a single favorite genre and mood as fixed preferences, which can over-favor a narrow slice of the catalog. A real recommender would need more diverse data, regular feedback from users, and checks for unequal exposure of artists and genres.

## Reflection

I learned that a recommender turns choices about data and weights into predictions. Even a simple rule can produce plausible results, but the result depends on what the system decides to measure. Giving genre a high weight makes the system feel sensible for a focused listener, but it can also prevent discovery outside that genre.

I also learned why explainability matters. The explanation makes it possible to inspect a recommendation instead of treating it as magic. In a larger system, that kind of transparency would help identify when the model is relying too heavily on one preference or overlooking part of a user's taste.
