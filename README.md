# MLB Hit Predictor

A ML project that predicts how many hits a Pirates player is expected to get in their next game, uses rolling batter statistics along with opposing starting pitcher matchup data pulled from Statcast with the help of pybaseball.

**Status: in progress.** Core pipeline and model are functional and are running on the full Pirates starting lineup (9 hitters). Currently identifying which features are worth keeping and where to add more predictive signal.

## Overview

I started this project as a simple binary classifier, predicting whether a player would get a hit in a given game. During this process, I was able to find and fix data leakage issues in my first version where randomly splitting the data let some future games end up in training instead of testing. This led me to rebuild the pipeline around chronological splits and creating rolling features that avoid leakage.

I've since shifted the goal from a yes/no hit predictor to something I believe is more useful and difficult: predicting the actual *number* of hits a player will get in a given game using Poisson regression, and Random Forest model for comparison.

## Approach

**Data source:** [pybaseball](https://github.com/jldbc/pybaseball), pulling per-pitch
Statcast data for each tracked hitter via `statcast_batter`.

**Pipeline:**
1. `get_team_data.py` - pulls raw Statcast data for each hitter over a given date range.
2. `clean_data.py` - filters to completed plate appearances, aggregates pitch-level data
   into one row per batter per game, and computes the target (`hits`) along with the
   starting pitcher's ID, handedness, and rest days for that game.
3. `add_hitter_stats.py` - adds rolling batter features (hits and plate appearances over
   the trailing 7 games), computed using only *prior* games to avoid leakage.
4. `add_pitcher_stats.py` - pulls the same season's data for every opposing starting
   pitcher faced, and builds rolling opponent-quality features (hit rate and strikeout
   rate allowed over their trailing 5 starts), merged onto the batter-game rows by
   pitcher ID and game.
5. `prep_for_model.py` - final encoding step (converting pitcher handedness to a binary
   feature) right before modeling.
6. `model.py` - trains and evaluates the models.

**Key design decisions:**
- **Chronological train/test split**, not random; the model is only ever tested on
  games that happened after its training data, to reflect realistic prediction
  conditions.
- **All rolling features use `.shift(1)`** before computing a rolling window, so a
  game's features never include that game's own outcome.
- **Only the starting pitcher** is used for opponent features, since that's the only
  pitcher matchup information actually knowable before a game begins.
- **Games with fewer than 2 plate appearances are excluded** from model training/testing
  (e.g. pinch-hit appearances), since they represent a fundamentally different, harder
  to predict scenario than a standard start.
- **Contact-quality stats (exit velocity, launch angle, etc.) from the game itself are
  deliberately excluded** as they're outcomes of the very at-bat being predicted, not
  information available beforehand.

## Modeling

Hits are modeled as a count (0, 1, 2, 3...) rather than a binary outcome, using:
- **Poisson regression**, with a player's recent plate-appearance rate as an exposure
  term, so the model separates "how many chances a player gets" from "how likely they
  are to get a hit per chance."
- **Random Forest Regressor**, for comparison and to check for feature interactions.
- A **naive baseline** (a player's own trailing 7-game hit rate, scaled by expected
  plate appearances) to check whether the trained models are adding real value over a
  simple heuristic.

Evaluated using MAE and Poisson deviance, rather than classification metrics.

## Current findings

- With a single-player dataset (~90 usable games), neither model beat the naive
  baseline, and no feature reached statistical significance which is a sign of too little
  data rather than a flawed approach.
- Expanding to the full 9-player lineup (482 training games, 121 test games) let both
  models beat the baseline for the first time (baseline MAE 0.692 vs. 0.667 for
  Poisson and 0.670 for Random Forest). Starting pitcher handedness also became the
  first statistically significant feature (p = 0.023) showing that facing a lefty was associated
  with fewer expected hits, a real, well-documented platoon effect. The model's pseudo
  R² is still low (~0.03), which given how much randomness is in a single game's
  outcome, is an expected result rather than a sign something's wrong.

## Next steps

- [ ] Add batter-specific platoon splits (hit rate vs. LHP/RHP separately), motivated
      directly by the significance of pitcher handedness above
- [ ] Evaluate whether `batter_rest_days` and `starting_pitcher_rest_days` are worth
      keeping, given their low significance and importance so far
- [ ] Investigate outlier values in `starting_pitcher_rest_days`
- [ ] Add ballpark factors using home/away team
- [ ] Add rolling, prior-games contact-quality features (e.g. trailing exit velocity)
- [ ] Build a script to generate predictions for an upcoming game's lineup, using
      probable starting pitchers rather than historical data

## Setup

```bash
pip install pandas numpy pybaseball scikit-learn statsmodels
python main.py
```

## What I learned

This project taught me the importance of thinking carefully about *when* information is
actually available in a real prediction scenario, not just whether it's correlated with
the outcome; the difference between a genuinely predictive feature and a leaked one is
often subtle. It also showed firsthand why more data can matter more than more features:
the same feature set that looked like noise with one player's data revealed a real,
interpretable effect once trained across the full lineup.