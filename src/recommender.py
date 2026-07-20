"""Simple, explainable music recommendation utilities."""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Song:
    """A song and the audio features used by the recommender."""

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """The preferences used to rank songs for one listener."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_values(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    user_genre: str,
    user_mood: str,
    target_energy: float,
    likes_acoustic: Optional[bool] = None,
) -> Tuple[float, List[str]]:
    """Apply the shared, transparent scoring recipe and return its reasons."""
    score = 0.0
    reasons: List[str] = []

    if genre.casefold() == user_genre.casefold():
        score += 3.0
        reasons.append(f"it matches your favorite genre ({genre})")
    if mood.casefold() == user_mood.casefold():
        score += 2.5
        reasons.append(f"it matches your preferred mood ({mood})")

    # Energy is on a 0--1 scale. A perfect match earns 2.5 points and the
    # reward smoothly decreases as the song moves away from the target.
    energy_similarity = max(0.0, 1.0 - abs(energy - target_energy))
    energy_points = 2.5 * energy_similarity
    score += energy_points
    if abs(energy - target_energy) <= 0.15:
        reasons.append("its energy is close to your target")

    if likes_acoustic is not None:
        acoustic_match = acousticness >= 0.5 if likes_acoustic else acousticness < 0.5
        if acoustic_match:
            score += 1.0
            preference = "more acoustic" if likes_acoustic else "less acoustic"
            reasons.append(f"it fits your preference for {preference} music")

    return score, reasons


class Recommender:
    """Object-oriented interface for scoring and ranking a catalog of songs."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        return _score_values(
            song.genre,
            song.mood,
            song.energy,
            song.acousticness,
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            user.likes_acoustic,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to ``k`` songs, highest score first."""
        if k <= 0:
            return []
        ranked = sorted(
            self.songs,
            key=lambda song: (-self._score_song(user, song)[0], song.title.casefold()),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Give a short human-readable explanation of a song's score."""
        score, reasons = self._score_song(user, song)
        if not reasons:
            return f"This is a lower-confidence suggestion with a score of {score:.2f}."
        return f"Recommended because {', '.join(reasons)} (score: {score:.2f})."


def load_songs(csv_path: str) -> List[Dict]:
    """Load the catalog CSV, converting numeric columns to useful Python types."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Song catalog not found: {path}")

    numeric_fields = {"id": int, "energy": float, "tempo_bpm": float,
                      "valence": float, "danceability": float, "acousticness": float}
    with path.open(newline="", encoding="utf-8") as catalog:
        reader = csv.DictReader(catalog)
        if not reader.fieldnames:
            return []
        return [
            {key: numeric_fields[key](value) if key in numeric_fields else value
             for key, value in row.items()}
            for row in reader
        ]


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one dictionary-form song against dictionary-form user preferences."""
    required_preferences = {"genre", "mood", "energy"}
    missing = required_preferences - user_prefs.keys()
    if missing:
        raise ValueError(f"Missing user preferences: {', '.join(sorted(missing))}")

    return _score_values(
        str(song["genre"]), str(song["mood"]), float(song["energy"]),
        float(song.get("acousticness", 0.0)), str(user_prefs["genre"]),
        str(user_prefs["mood"]), float(user_prefs["energy"]),
        user_prefs.get("likes_acoustic"),
    )


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Return dictionary-form recommendations with their scores and explanations."""
    if k <= 0:
        return []

    ranked = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = (
            f"Recommended because {', '.join(reasons)}."
            if reasons else "A lower-confidence suggestion based mainly on energy."
        )
        ranked.append((song, score, explanation))

    ranked.sort(key=lambda item: (-item[1], str(item[0]["title"]).casefold()))
    return ranked[:k]
