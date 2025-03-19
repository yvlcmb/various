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
  
  let domestication = createCard "domestication" 1 "yellow" (None, Some "castle", Some "castle", Some "castle") "castle"
