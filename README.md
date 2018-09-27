# Terminal-Blackjack
Terminal-based Blackjack game - with betting!

## What is this?

Play Blackjack in your UNIX terminal! Just like real Blackjack, you start out with chips, and place bets per round. The dealer deals to you and then to itself. The winner takes all! 

## Requirements
Have Python3 installed. Python2 should be supported but not tested. Only the native `random` package is used.

## Getting Started
To launch the game, type 

```python BlackJack.py``` 

You will be greeted with the interface 

```===== Welcome to ♠ BlackJack =====``` 

You will start out with the default 500 chips: 

```You have 500 chips.``` 

Then, following the prompt, 

```Press s to start or q to quit```

press `s` and then hit `enter` to `start` or press `q` and `enter` to quit. Since inputs use the python default `input` command, (no fancy pygame GUI this time, sorry!) be sure to press enter afterwards.

## Blackjack Rules
The same rules of blackjack apply here, getting as close to 21 as possible without busting (going over). However, common practices, as per wikipedia, such as buying insurance, surrendering, doubledown, and split, are not implemented. Also, the player sees the starting hand of the dealer.

## How to Play

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
When prompted with 
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
The game is implemented in python, using custom classes denoting a card, hand, and deck. Only a simple vector-based (dynamic array) list data structure are used for this program, since we only need to keep track of sets of cards. Each card has a rank and suit, both of which are global constants stored in a dictionary and list, respectively. The rank dictionary will map the rank character to its corresponding blackjack value. We only use this map for non-Ace cards. Each deck is a list of cards that is shuffled during initiation. Each hand will contain a list of cards as well as the optimal total card sum, taking into account the dual values of an Ace. Each time an ace is dealt, we keep track of the number of aces that we denote as `11`s so when the hand goes over, we can lower their values to `1`.

Since the game is single player, only one deck is used, and each round reinstantiates the deck with a full set of cards so we never run out. However, during one instantiation of the game program, you start with a fixed number of chips that will last until you quit or run out. Your chip count never resets unless the program restarts.

Each round of dealing will update the hand `value` as well as a `twentyone` boolean that determines whether the hand has reached `blackjack`. These two variables determines the result of each dealing and whether to prompt for more hits.

The dealer AI will choose to deal or hold depending on its value only, to model a real game setting where more than one player plays and to make the game easier. To model a real-life decision setting, there is a `RISK` variable that denotes the risk-taking behavior of the dealer. The program determines whether the dealer hits by taking a random integer between 1 and 1000 and seeing if it is less than the risk variable divided by `n`, a factor based on how close the current hand value is to `21`. Therefore, the dealer will stand unless 
```
randint < RISK / n
```
The higher the `RISK` constant, the more likely the dealer will take risks by hitting. Feel free to change this global constant to change up the dealer playstyle. The current value is set to `500` for a very conservative player.

Of course, we could implement the dealer AI to take into account the player hand, but since there is only 1 player, that means the dealer will always deal if his hand has less value than the player's, leading to much less variation in playstyle.




