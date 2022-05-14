import sys
from tenis import game

def main(args=None):
  if args is None:
    args = sys.argv[1:]

  app = game.Game()
  app.run()

if __name__ == '__main__':
  sys.exit(main())