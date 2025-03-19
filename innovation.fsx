/// <summary>
/// Innovation by C. Chudyk
/// </summary>

module Innovation = 
  
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
  let theWheel = { name = "The Wheel"; 
                   age = 1;
                   color = "green"; 
                   icons = (None, Some "castle", Some "castle", Some "castle");
                   dogma_icon = "castle" }
