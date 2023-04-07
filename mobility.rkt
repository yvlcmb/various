#lang racket
(define (main)
  (define stryker (hash "weight" 36320 "axles" 4))
  (= (factor-weight stryker) 0.314622))

(define (factor-weight vehicle)
  #|
  :param vehicle: hash table of vehicle properties
  :return: a number reflecting the vehicle's weight factor
  |#
  (local ((define lbs/axle (/ (hash-ref vehicle "weight") (hash-ref vehicle "axles")))
          (define kips (/ (hash-ref vehicle "weight") 1000)))
  (let ([mods (cond
                [(< lbs/axle 2000)  `(0.533 0)]
                [(< lbs/axle 13500) `(0.033 1.05)]
                [(< lbs/axle 20000) `(0.142 -0.42)]
                [else `(0.278 -3.115)])])
  (+ (* (first mods) (/ kips (hash-ref vehicle "axles")) (last mods))))))

(display (main))