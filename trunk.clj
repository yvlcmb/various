(def book (slurp "https://gutenberg.org/cache/epub/98/pg98.txt"))

(def words (re-seq #"[\w|']+" book))

(def common-words #{"a" "able" "about" "across" "after" "all" "almost"
                    "also" "am" "among" "an" "and" "any" "are" "as" "at" "be" "been"
                    "because" "but" "by" "can" "cannot" "could" "else"
                    "dear" "did" "do" "does" "ever" "every" "for" "from"
                    "get" "got" "had" "has" "have" "he" "hers" "him"
                    "i" "if" "in" "into" "is" "it" "its" "just" "least"
                    "let" "like" "likely" "may" "mr" "me" "might" "most" "must"
                    "neither" "no" "nor" "not" "now" "of" "off" "often" "on"
                    "one" "only" "or" "other" "our" "own" "rather"
                    "say" "says" "she" "should" "since" "so" "some" "than"
                    "that" "the" "their" "them" "then" "there" "they" "this"
                    "those" "tis" "to" "too" "twas" "up" "upon" "us" "wants"
                    "was" "we" "were" "what" "where" "which" "while" "who"
                    "when" "her" "with" "his" "my" "said" "s" "down" "out"
                    "man" "woman" "miss" "here" "way" "old" "these" "day" "good"
                    "himself" "herself" "before" "see" "never" "always" "t"
                    "again" "more" "such" "over" "under" "muchk" "how" "through"
                    "whom" "why" "will" "wih" "would" "yet" "you" "come" "your" "very"})

; 20 most frequently used words
; -----------------------------
(def top-25 (->> words
                 (map clojure.string/lower-case)
                 (remove common-words)
                 (frequencies)
                 (sort-by val)
                 (take-last 25)))

(println top-25)


