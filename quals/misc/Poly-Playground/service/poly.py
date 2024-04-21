#!/usr/local/bin/python

import numpy as np
from decimal import Decimal

MAX_ROOT = 5
TESTS_PER_ROOT = 20

DASH_SEPARATOR = "-"*20

print(
"""Welcome to the Polynomial Playground, where you'll embark on an exhilarating journey of polynomial creation! Get ready to flex your mathematical muscles as you craft intricate equations from a given set of roots. Are you up for the challenge?

In this mind-bending adventure, your task is to construct polynomials using a set of provided roots. Armed with your mathematical prowess and creativity, you'll delve into the world of polynomial composition and unlock the secrets of equation crafting.

From simple quadratics to complex higher-degree polynomials, each level presents a new set of roots waiting to be transformed into an elegant equation. But don't be fooled by the simplicity of the task; as you progress, the challenge will intensify, requiring you to employ strategic thinking and mathematical precision.

How to Play:
1. You'll be given a set of `n` roots for each level.
2. Utilize your mathematical knowledge to construct a polynomial equation that has the provided roots. You can assume that repeated roots will be given as repeats.
3. Channel your creativity and problem-solving skills to craft elegant and efficient equations.
4. Submit your polynomial creations as a comma-separted list of `n+1` coefficients starting with the highest order (which should always be 1).

Are you ready to unleash your inner mathematician and become a master polynomial architect? Prepare to explore the depths of equation construction, unlock the beauty of mathematical expression, and emerge victorious in the Polynomial Playground! 

Here's your first problem..."""
)
print(DASH_SEPARATOR)


class WrongAnswerException(Exception):
    def __init__(self, message=""):
        super().__init__(message)
        self.message = message
try:
  t = 1
  for num_poly in range(1, MAX_ROOT + 1):
      for n in range(TESTS_PER_ROOT):
          print(f"Level {t}:")
          roots = np.random.randint(low=-1000, high=1001, size=num_poly)
          print("Roots:", ",".join(map(lambda r: str(r), roots)))
          poly_coeffs = np.poly(list(map(lambda x:Decimal(x.item()),roots)))
          input_coeff = input("Present the coefficients of your amazing equation: ")
          answers = list(map(lambda x:Decimal(x),input_coeff.split(",")))
          if len(answers) != len(poly_coeffs):
             raise WrongAnswerException(f"Wrong number of coefficients given! Expected {len(poly_coeffs)}, given {len(answers)}. Return to Polynomial Academy before trying again! >.<")
          if not (answers == poly_coeffs).all():
             raise WrongAnswerException(f"Wrong answer! You should've gotten {','.join(map(lambda x:str(int(x)),poly_coeffs))}. Return to Polynomial Academy before trying again! >.<")
          t += 1
          print(DASH_SEPARATOR)

  print("Congratulations you have succeeded in the treacherous Polynomial Playground! Here's your flag!")
  with open("flag.txt") as f:
      print(f.readline())
except WrongAnswerException as e:
   print(e.message)
except Exception as e:
   print("You failed! I can't even understand what you gave me! Return to Polynomial Academy before trying again! >.<")
