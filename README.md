# Terminal-Blackjack
Terminal-based Blackjack game - with betting!

## What is this?

Play Blackjack in your UNIX terminal! Just like real Blackjack, you start out with chips, and place bets per round. The dealer deals to you and then to itself. The winner takes all! 

## Requirements
Have Python3 installed. Python2 should be supported but not tested. Only the native `random` package is used.

## Instructions
To launch the game, type 

```python BlackJack.py``` 

You will be greeted with the interface 

```===== Welcome to ♠ BlackJack =====``` 

You will start out with the default 500 chips: 

```You have 500 chips.``` 

Then, following the prompt, 

```Press s to start or q to quit```

press `s` and then hit `enter` to `start` or press `q` and `enter` to quit. Since inputs use the python default `input` command, (no fancy pygame GUI this time, sorry!) be sure to press enter afterwards.

## How to play

When given the prompt
```Place your bet:``` enter the integer number of chips to bet. The game will start with a starting hand
```
---Dealer hand---
♥ 5 
♥ A 
---Player Hand---
♠ 10 
♣ A 
```
The same rules of blackjack apply here, getting as close to 21 as possible without busting (going over). When prompted with 
```
Hit or Stand?
(Press enter to hit, other key to stand)
```
Press `enter` to continue hitting, enter any other key to stand.

As long as you did not bust, you will continue to be prompted with this message. Otherwise, you will likely see something like
```
---Player Hand---
♠ 5 
♥ 10 
♥ Q 
Bust! Dealer wins...
You have 453 chips.
```
Note that even if you got `blackjack`, the dealer will still proceed to deal to itself since it may get blackjack. If you choose to stand, the dealer will proceed to choose to stand or hit. The dealer may choose to stand, in which case you may see
```
Dealer stands!
Comparing hands...
Dealer has bigger hand. Player loses...
```

Or if the dealer chooses to hit

```
Dealer's turn to play...
Dealer hits!
---Dealer hand---
♠ Q 
♣ 10 
♣ 3 
Dealer busts! Player wins the round!
```
After each round, you will be told how many chips you currently have. 
```
You have 450 chips.

Press s to start or q to quit
```

If you lost all your chips, then its game over...
```
No more chips, ending game...
```
## Design and Implementation
The game is implemented in python, using custom classes denoting a card, hand, and deck. Each deck is a list of cards that is shuffled during initiation. Each hand will contain a list of cards as well as the optimal total card sum, taking into account the dual values of an Ace. 

