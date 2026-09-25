# MLB Hit Predictor

A ML project that predicts how many hits each Pirates starting hitter is expected to get in their next game, using rolling batter statistics along with opposing starting pitcher matchup data pulled from Statcast with the help of pybaseball.

**Status: V1 complete.** The full pipeline trains on the 2026 season for the 9-man Pirates lineup, and `predict_today.py` generates hit predictions for the day's game using the opponent's probable starting pitcher. This version is finished and no longer under active development.

## Overview

I started this project as a simple binary classifier, predicting whether a player would get a hit in a given game. During this process, I was able to find and fix data leakage issues in my first version where randomly splitting the data let some future games end up in training instead of testing. This led me to rebuild the pipeline around chronological splits and creating rolling features that avoid leakage.

I then shifted the goal from a yes/no hit predictor to something I believe is more useful and difficult: predicting the actual *number* of hits a player will get in a given game using Poisson regression, with a Random Forest model for comparison. V1 ends with a working present-day prediction script that pulls the day's matchup live from the MLB Stats API.

## Approach

**Data sources:** [pybaseball](https://github.com/jldbc/pybaseball) for per-pitch Statcast data (`statcast_batter`, `statcast_pitcher`), and the public [MLB Stats API](https://statsapi.mlb.com) for today's schedule, probable pitchers, and pitcher handedness.

**Training pipeline** (run by `main.py`):
1. `get_team_data.py` - looks up each tracked hitter's MLBAM ID, pulls their raw Statcast data over the season's date range, and saves the lineup IDs to `data/lineup_ids.csv`.
2. `clean_data.py` - filters to completed plate appearances, aggregates pitch-level data into one row per batter per game, and computes the target (`hits`) along with the starting pitcher's ID and handedness for that game.
3. `add_pitcher_stats.py` - pulls the same season's data for every opposing starting pitcher faced, and builds rolling opponent-quality features (hit rate and strikeout rate allowed over their trailing 5 starts), merged onto the batter-game rows by pitcher ID and game.
4. `add_hitter_stats.py` - adds rolling batter features over the trailing 7 games: hits, plate appearances, overall hit rate, and platoon splits (hit rate vs. LHP and vs. RHP), computed using only *prior* games to avoid leakage.
5. `prep_for_model.py` - final encoding step (converting pitcher handedness to a binary feature) right before modeling.
6. `model.py` - trains and evaluates the models, and `main.py` saves them to `poisson_model.pkl` and `rf_model.pkl`.

**Prediction** (`predict_today.py`):
1. Finds today's Pirates game and the opponent's probable starting pitcher from the MLB Stats API.
2. Looks up that pitcher's handedness and builds their trailing-5-start hit and strikeout rates from recent Statcast data.
3. Builds each tracked hitter's trailing-7-game features from the training data.
4. Prints predicted hits per hitter from both the Poisson and Random Forest models.

**Key design decisions:**
- **Chronological train/test split**, not random; the model is only ever tested on games that happened after its training data, to reflect realistic prediction conditions.
- **All rolling features use `.shift(1)`** before computing a rolling window, so a game's features never include that game's own outcome.
- **Only the starting pitcher** is used for opponent features, since that's the only pitcher matchup information actually knowable before a game begins.
- **Games with fewer than 2 plate appearances are excluded** from model training/testing (e.g. pinch-hit appearances), since they represent a fundamentally different, harder to predict scenario than a standard start.
- **Contact-quality stats (exit velocity, launch angle, etc.) from the game itself are deliberately excluded** as they're outcomes of the very at-bat being predicted, not information available beforehand.

## Modeling

Hits are modeled as a count (0, 1, 2, 3...) rather than a binary outcome, using:
- **Poisson regression**, with a player's recent plate-appearance rate as an exposure term, so the model separates "how many chances a player gets" from "how likely they are to get a hit per chance."
- **Random Forest Regressor**, for comparison and to check for feature interactions.
- A **naive baseline** (a player's own trailing 7-game hit rate, scaled by expected plate appearances) to check whether the trained models are adding real value over a simple heuristic.

**Final features:** `hits_last_7`, `pa_last_7`, `hit_rate_last_7`, `hit_rate_vs_L_last_7`, `hit_rate_vs_R_last_7`, `opp_hit_rate_last_5`, `opp_k_rate_last_5`, `starting_pitcher_hand_L`.

Evaluated using MAE and Poisson deviance, rather than classification metrics.

## Results (V1)

Trained on 496 batter-games (through Aug 26, 2026) and tested on 125 later batter-games (Aug 29 - Sep 23, 2026):

| Model | MAE | Poisson deviance |
|---|---|---|
| Naive baseline | 0.697 | - |
| **Poisson regression** | **0.639** | **0.910** |
| Random Forest | 0.649 | 0.914 |

- Both models beat the naive baseline, with Poisson regression performing best (about an 8% reduction in MAE).
- **Starting pitcher handedness** remained statistically significant (p = 0.026): facing a lefty was associated with fewer expected hits, a real, well-documented platoon effect. A hitter's recent hit rate was also significant (p = 0.045).
- The Random Forest leaned most heavily on the opposing pitcher's recent strikeout and hit rates, followed by the batter's platoon splits.
- The model's pseudo R² is still low (~0.02), which given how much randomness is in a single game's outcome, is an expected result rather than a sign something's wrong.

## How the model evolved

- With a single-player dataset (~90 usable games), neither model beat the naive baseline, and no feature reached statistical significance which is a sign of too little data rather than a flawed approach.
- Expanding to the full 9-player lineup let both models beat the baseline for the first time, and pitcher handedness became the first significant feature.
- Motivated by that result, I added batter-specific platoon splits (hit rate vs. LHP/RHP). I tested a 15-game window for these but kept 7 games, and dropped `batter_rest_days` and `starting_pitcher_rest_days` after they consistently showed low significance and importance.

## Setup

```bash
pip install -r requirements.txt
python main.py           # pulls season data, builds features, trains and saves the models
python predict_today.py  # predicts hits for today's Pirates game
```

The trained `.pkl` models aren't committed, so run `main.py` at least once before `predict_today.py`. To predict with up-to-date hitter form, update `END_DATE` in `main.py` and rerun it first. The season date range and tracked lineup are set in `main.py` and `get_team_data.py`.

## Known limitations

- `predict_today.py` needs the opponent's probable starter to be announced, and only handles the first game of a doubleheader.
- The tracked lineup is fixed to 9 hitters rather than pulled from the day's actual lineup card.
- A single season of data for 9 players is still a small sample for a sport this noisy.

## Ideas for a future version

- Ballpark factors using home/away team
- Rolling, prior-games contact-quality features (e.g. trailing exit velocity)
- Pulling the actual starting lineup for each game automatically
- Multiple seasons and more teams for a larger training set

## What I learned

This project taught me the importance of thinking carefully about *when* information is actually available in a real prediction scenario, not just whether it's correlated with the outcome; the difference between a genuinely predictive feature and a leaked one is often subtle. It also showed firsthand why more data can matter more than more features: the same feature set that looked like noise with one player's data revealed a real, interpretable effect once trained across the full lineup.
