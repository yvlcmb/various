/// <summary>
/// Innovation by C. Chudyk
/// </summary>

module Innovation = 
  open System.Collections.Generic
  type IconTuple = string option * string option * string option * string option 

  type Card = {
      name: string
      age: int
      color: string
      icons: IconTuple
      dogma_icon: string
  }

  let createCard 
     (name: string)
     (age: int)
     (color: string)
     (icons: IconTuple) 
     (dogma_icon: string) : Card =
     { name = name
       age = age
       color = color
       icons = icons
       dogma_icon = dogma_icon }

  /// sample cards
  let domestication = createCard "domestication" 1 "yellow" (None, Some "castle", Some "castle", Some "castle") "castle"
  let metalWorking = { domestication with name = "Metal Working"; color = "red" } 
  let mysticism = { domestication with name = "Mysticism"; color = "purple" }
  let theWheel = { name = "The Wheel"; 
                   age = 1;
                   color = "green"; 
                   icons = (None, Some "castle", Some "castle", Some "castle");
                   dogma_icon = "castle" }

// Define the Player record with immutable fields
type Player = {
    Hand: Map<string, Card>  // Use Map for an immutable hand
    Board: Map<string, { Cards: Queue<Card>; Splay: string }>  // Board is a Map where each color has a Queue of cards
    ScorePile: List<Card>  // Score pile is a List of cards
    Achievements: List<string>  // List of achievements
}

let createPlayer () : Player =
    let initialBoard = 
        Map.ofList [
            ("red", { Cards = Queue<Card>(); Splay = "none" })
            ("yellow", { Cards = Queue<Card>(); Splay = "none" })
            ("green", { Cards = Queue<Card>(); Splay = "none" })
            ("blue", { Cards = Queue<Card>(); Splay = "none" })
            ("purple", { Cards = Queue<Card>(); Splay = "none" })
        ]
    
    {
        Hand = Map.empty
        Board = initialBoard
        ScorePile = []
        Achievements = []
    }


let meld (player: Player) (cardName: string) : Player =
    match Map.tryFind cardName player.Hand with
    | None ->
        printfn "card not in hand"
        player  // Return the unchanged player if the card was not found
    | Some card ->
        // Remove the card from the hand (create a new hand without the card)
        let newHand = Map.remove cardName player.Hand
        
        // Get the color and the corresponding stack on the board
        let color = card.Color
        let boardStack = player.Board.[color]
        
        // Add the card to the corresponding color stack's cards (create a new queue)
        let newQueue = Queue<Card>(boardStack.Cards)
        newQueue.Enqueue(card)
        
        // Create a new board with the updated queue for the color
        let newBoard = Map.add color { Cards = newQueue; Splay = boardStack.Splay } player.Board
        
        // Print the meld information
        printfn "%s melded to %s stack" card.Name color
        
        // Return a new Player with the updated hand and board
        { player with Hand = newHand; Board = newBoard }

// Example usage
let player = createPlayer()

// Add cards to player's hand (by creating a new map)
let playerWithHand = { player with Hand = Map.add domestication.Name card1 player.Hand }
let playerWithMoreCards = { playerWithHand with Hand = Map.add theWheel.Name card2 playerWithHand.Hand }

// Perform a meld
let playerAfterMeld = meld playerWithMoreCards "red"

// Print player state after meld
printfn "Hand size: %d" (playerAfterMeld.Hand |> Map.count)
printfn "Cards in red stack: %d" (playerAfterMeld.Board.["red"].Cards.Count)
