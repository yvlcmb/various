#lang scheme
;from wadehuber's youtube tutorial

(define saints2009
  '(
    (drew-brees . ((passing . 4338 ) (rushing . 33) (receiving . -4)))
    (reggie-bush . ((rushing . 390) (receiving . 335)))))

(define find-player
  (lambda (lst player)
    (cond
      ((null? lst) '())
      ((equal? (car (car lst)) player) (cdr (car lst)))
      (else (find-player (cdr lst) player)))))

; racket version below:
#;(define (find-player2 lst player)
    (cond
      [(null? lst) '()]
      [(equal? (first (first lst)) player) (rest (first lst))]
      [else (find-player (rest lst) player)]))

(find-player saints2009 'drew-brees)

(newline)
"find-player-stat returns a specific statistic for a player"
(define find-stat
  (lambda (lst stat)
    (cond
      ((null? lst) 0)
      ((equal? stat (car (car lst))) (cdr (car lst)))
      (else (find-stat (cdr lst) stat)))))
(define find-player-stat
  (lambda (lst player stat)
    (find-stat (find-player lst player) stat)))
(find-player-stat saints2009 'reggie-bush 'rushing)

(newline)
"find-team-stat fins the team total statistics"
(define find-team-stat
  (lambda (lst stat)
    (if (null? lst)
        0
        (+ (find-stat (cdr (car lst)) stat) (find-team-stat (cdr lst) stat)))))
(find-team-stat saints2009 'passing)

(newline) 
(define some-pairs '((passing . 4338) (rushing . 33)))
(assoc 'passing some-pairs)

(call-with-output-file "/home/develop/db-in-scheme.txt"
  (lambda (output-port)
    (display (find-team-stat saints2009 'passing) output-port)))
