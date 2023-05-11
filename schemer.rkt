#lang racket
#| some examples from The Little Schemer, implemented in Racket |#

;; required for the rest of the functions
(define (atom? x)
  (and (not (null? x)) 
       (not (pair? x))))

;; return the leftmost item in a nested list
(define (leftmost l)
  (cond
    [(atom? (first l)) (first l)]
    [else (leftmost (first l))]))

;; return the rightmost item in a nested list
(define (rightmost x)
  (cond
    [(atom? (last x)) (last x)]
    [else (rightmost (last x))]))

;; remove an item (`remove member`) from a list
(define (rember* a l)
    (cond
      [(null? l) null]
      [(atom? (first l))
       (cond
         [(equal? (first l) a)
          (rember* a (rest l))]
         [else (cons (first l) (rember* a (rest l)))])]
      [else (cons (rember* a (first l)) (rember* a (rest l)))]))

;; insert an item into the list to the right of an item in that list
(define (insertR* new old l)
    (cond
      [(null? l) null]
      [(atom? (first l))
        (cond 
           [(eq? (first l) old) (cons old (cons new (insertR* new old (rest l))))]
           [else  (cons (first l) (insertR* new old (rest l)))])]
       [else (cons (insertR* new old (first l)) (insertR* new old (rest l)))]))

;; count how many times an item occurs in a list 
(define (occur* a l)
    (cond
      [(null? l) 0]
      [(atom? (first l))
       (cond
         [(eq? (first l) a)
          (add1 (occur* a (rest l)))]
         [else
           (occur* a (rest l))])]
      [else
        (+ (occur* a (first l))
           (occur* a (rest l)))]))

;; alternative approach to count how many times an item occurs in a list, from Caleb Tebbe
(define (count-occurrences s slist) 
    (cond [(null? slist) 0]
          [(list? (car slist)) ; first element is a list so add its result with rest of the list
           (+ (count-occurrences s (car slist))
              (count-occurrences s (cdr slist)))]
          [(eq? s (car slist)) ; found s, add 1 to result on rest of list
           (+ 1 (count-occurrences s (cdr slist)))]
          [else (count-occurrences s (cdr slist))])) ; no results on the first element recurse on rest of list

;; alternative approach to count how many times an item occurs in a list
(define (count-atoms a s) 
  (cond
    [(empty? s) 0]
    [(list? (first s)) (+ (count-atoms a (first s)) (count-atoms a (rest s)))]
    [(equal? a (first s)) (add1 (count-atoms a (rest s)))]
    [else (count-atoms a (rest s))]))

;; find if an item is in a nested list 
(define (memb a s)
    (cond
      [(empty? s) #f]
      [(member a (first s)) #t]
      [else (memb a (rest s))]))

;; alternative way to find if an item is in a nested list, from Oscar Lopez
(define (atom-occur? a s)
    (cond
      [(empty? s) #f]
      [(not (pair? s)) (equal? a s)]
      [else (or (atom-occur? a (first s))
                (atom-occur? a (rest s)))]))


#| testing section |#
(define ingredients '(((("hot") ("tuna" ("and")))) "cheese"))
(define banana-split '(("banana") ("split" (((("banana" "ice"))) ("cream" ("banana"))))))
(define coffee-notes '('sweet-fruit 'red-fruit 'chocolate 'floral 'spice 'citrus 'smoke 'tobacco 'tea 'nut))
;;^ what is the difference between using values and strings?

(leftmost ingredients) ;hot
(rightmost ingredients) ;cheese
(rember* "tuna" '("hot" "tuna")) ;'("hot")
(insertR* "pickles" "cheese" ingredients) ;'(((("hot") ("tuna" ("and")))) "cheese" "pickles")
(equal? (list (occur* "banana" banana-split)
              (count-atoms "banana" banana-split)
              (count-occurrences "banana" banana-split))
        '(3 3 3)) ;#t
(atom-occur? "banana" banana-split) ;#t
(memb "banana" banana-split) ;#t
