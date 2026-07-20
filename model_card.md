# 🎧 Model Card: VibeMatch 1.0

## 1. Model Name

**VibeMatch 1.0**

## 2. Intended Use

VibeMatch 1.0 is a classroom music recommender that suggests songs from a small catalog based on a listener's stated genre, mood, energy, and acousticness preferences. It is intended for learning how recommendation systems turn features into ranked results, not for making production recommendations to real users.

It assumes that a listener can describe their taste with one favorite genre, one preferred mood, a target energy level, and a simple acousticness preference. Real music taste is more complicated and changes by situation, so this assumption is intentionally limited.

## 3. How the Model Works

Each song is described by genre, mood, energy, tempo, valence, danceability, and acousticness. The recommender currently uses genre, mood, energy, and acousticness. A genre match is worth 3 points, a mood match is worth 2.5 points, energy similarity is worth up to 2.5 points, and a matching acousticness preference is worth 1 point.

The system compares every song to the user's profile, adds the matching points, and sorts the songs by total score. It also explains which matches helped each recommendation. The energy score changes gradually instead of being all-or-nothing, so a song that is close to the target energy still receives credit.

## 4. Data

The catalog contains 10 fictional songs. It includes pop, lofi, rock, ambient, jazz, synthwave, and indie pop, with moods such as happy, chill, intense, relaxed, focused, and moody. I did not add or remove catalog entries.

The dataset is too small and too selective to represent musical taste fairly. It does not include lyrics, language, cultural context, release date, artist popularity, or listener feedback. Several genres and moods appear only once, which makes them harder to recommend.

## 5. Strengths

The recommender works best for listeners whose favorite genre and mood are represented in the catalog. For example, a pop, happy, high-energy profile ranks `Sunrise City` first because it matches both categories and has very similar energy. The scoring rule is easy to inspect, and the explanations show why a song appears near the top.

It also handles near matches better than a strict filter because energy similarity changes smoothly. A song does not need to match every preference to be considered.

## 6. Limitations and Bias

The model can over-focus on the one genre and mood provided by the user, which may reduce discovery and repeatedly favor the same kinds of songs. Genres with more entries have more chances to appear in results, while a genre represented by one song has less opportunity. The selected weights are subjective; changing them changes what the recommender considers important.

It does not learn from skips, repeats, playlists, or ratings. It also cannot understand lyrics, artists, cultural meaning, or a listener's changing context. Because the catalog is fictional and tiny, it should not be used to draw conclusions about real users or music audiences.

## 7. Evaluation

I tested a pop/happy profile with a target energy of 0.8 and a preference for less acoustic music. I checked that the energetic, happy pop track ranked first and that other close matches followed it. I also used the included tests to confirm that the object-oriented recommender returns songs in score order and produces a non-empty explanation.

The main result was that the scoring behavior was easy to predict once the weights were clear. This was useful for debugging, but it also showed how strongly a designer's weight choices affect the recommendations.

## 8. Future Work

Future versions could use tempo, valence, and danceability; accept multiple favorite genres and moods; learn from ratings; and add a diversity rule so the top results are not too similar. A larger and more balanced catalog would improve coverage. It could also explain tradeoffs, such as why a song was recommended despite not matching the favorite genre.

## 9. Personal Reflection

Building this project showed me that recommendation systems are not neutral: the data fields and scoring weights decide what the system notices. A simple recommender can feel convincing even when it is based on only a few rules. I found the explanations especially helpful because they made the ranking understandable and made it easier to see where bias or overly narrow preferences could enter the system.
