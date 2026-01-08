"""
Deck and card management for poker trainer.
"""
import random
from enum import Enum
from dataclasses import dataclass
from typing import List


class Suit(Enum):
    """Card suits."""
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'


class Rank(Enum):
    """Card ranks with values."""
    TWO = (2, '2')
    THREE = (3, '3')
    FOUR = (4, '4')
    FIVE = (5, '5')
    SIX = (6, '6')
    SEVEN = (7, '7')
    EIGHT = (8, '8')
    NINE = (9, '9')
    TEN = (10, 'T')
    JACK = (11, 'J')
    QUEEN = (12, 'Q')
    KING = (13, 'K')
    ACE = (14, 'A')

    def __init__(self, rank_value: int, symbol: str):
        self.rank_value = rank_value
        self.symbol = symbol


@dataclass(frozen=True)
class Card:
    """Represents a single playing card."""
    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        """String representation (e.g., 'A♠', 'K♥')."""
        return f"{self.rank.symbol}{self.suit.value}"

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other: 'Card') -> bool:
        """Compare cards by rank value."""
        return self.rank.rank_value < other.rank.value

    def __eq__(self, other) -> bool:
        """Cards are equal if rank and suit match."""
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self) -> int:
        """Make card hashable."""
        return hash((self.rank, self.suit))


class Deck:
    """Standard 52-card deck."""

    def __init__(self):
        """Initialize a full deck of 52 cards."""
        self.cards: List[Card] = []
        self.reset()

    def reset(self):
        """Reset deck to full 52 cards."""
        self.cards = [
            Card(rank, suit)
            for suit in Suit
            for rank in Rank
        ]

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self, count: int = 1) -> List[Card]:
        """
        Deal cards from the deck.

        Args:
            count: Number of cards to deal

        Returns:
            List of dealt cards

        Raises:
            ValueError: If not enough cards in deck
        """
        if count > len(self.cards):
            raise ValueError(f"Not enough cards in deck. Requested {count}, have {len(self.cards)}")

        dealt = self.cards[:count]
        self.cards = self.cards[count:]
        return dealt

    def deal_one(self) -> Card:
        """Deal a single card."""
        return self.deal(1)[0]

    def remove_cards(self, cards: List[Card]):
        """Remove specific cards from deck (useful for scenarios)."""
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)

    def __len__(self) -> int:
        """Return number of cards remaining in deck."""
        return len(self.cards)

    def __str__(self) -> str:
        return f"Deck({len(self.cards)} cards)"


def parse_card(card_str: str) -> Card:
    """
    Parse a card from string notation (e.g., 'As', 'Kh', 'Tc').

    Args:
        card_str: Two-character string (rank + suit)

    Returns:
        Card object

    Raises:
        ValueError: If card string is invalid
    """
    if len(card_str) != 2:
        raise ValueError(f"Invalid card string: {card_str}")

    rank_str, suit_str = card_str[0].upper(), card_str[1].lower()

    # Map suit characters
    suit_map = {
        'h': Suit.HEARTS,
        'd': Suit.DIAMONDS,
        'c': Suit.CLUBS,
        's': Suit.SPADES
    }

    if suit_str not in suit_map:
        raise ValueError(f"Invalid suit: {suit_str}")

    # Find rank by symbol
    rank = None
    for r in Rank:
        if r.symbol == rank_str:
            rank = r
            break

    if rank is None:
        raise ValueError(f"Invalid rank: {rank_str}")

    return Card(rank, suit_map[suit_str])


def parse_cards(cards_str: str) -> List[Card]:
    """
    Parse multiple cards from space-separated string.

    Args:
        cards_str: Space-separated cards (e.g., 'As Kh Qd')

    Returns:
        List of Card objects
    """
    return [parse_card(card) for card in cards_str.split()]
