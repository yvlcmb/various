#lang racket
#| Calculate mobility index and one pass vehicle cone index for wheeled vehicles

Sources:
  Wong J.Y., Jayakumar P., Toma E., & Preston-Thomas, J. (2020).
     A review of mobility metrics for next generation vehicle mobility models.
     Journal of Terramechanics (87). 11 -20.
  U.S. Department of the Army. (1994). Planning and design of roads, airfields,
     and heliports in the theater of operations --airfield and heliport design:
     FM 5-430-00-1/AFPAM 32-8013, Vol 1.
     
Vehicle specs from https://en.wikipedia.org/wiki/Stryker
|#
(require rackunit)

(define (test-factors)
  (define stryker (hash "weight" 36320  ;lbs
                        "clearance" 21  ;inches
                        "axles" 4
                        "wheel#" 8
                        "tire-width" 22  ;inches
                        "hydraluic" #t
                        "tire-diameter" 45  ;inches
                        "tire#" 8))
  (check-equal? (factor-weight stryker) 0.314622)
  (check-equal? (exact->inexact(factor-wheel-load stryker)) 4.54)
  (check-equal? (factor-grouser stryker) 1)
  (check-equal? (exact->inexact (factor-tire stryker)) 3.125)
  (check-equal? (factor-transmission stryker) 1.05)
  (check-equal? (factor-engine stryker) 1)
  (check-equal? (exact->inexact (factor-contact-pressure stryker)) 9.171717171717171)
  (check-equal? (exact->inexact (factor-clearance stryker)) 2.1)
  (check-equal? (calculate-mobility-index stryker) 3.531569664))

(define (calculate-vci-1 vehicle)
  #|
  :param vehicle: hash table of vehicle properties
  :return: the one-pass vehicle cone index for fine-grained soils
  |#
  (define mi (calculate-mobility-index vehicle))
  (- (+ 7 (* 0.2 mi) (/ 39.2 (+ mi 5.6)))))

(define (calculate-mobility-index vehicle)
  #|
  :param vehicle: hash table of vehicle properties
  :return: a number reflecting the vehicle's mobility index
  |#
  (* (- (+ (/ (* (factor-contact-pressure vehicle) (factor-weight vehicle))
              (* (factor-tire vehicle) (factor-grouser vehicle)))
           (factor-wheel-load vehicle))
        (factor-clearance vehicle))
     (* (factor-engine vehicle) (factor-transmission vehicle))))

(define (factor-weight vehicle)
  (local ((define lbs/axle (/ (hash-ref vehicle "weight") (hash-ref vehicle "axles")))
          (define kips (/ (hash-ref vehicle "weight") 1000)))
  (let ([mods (cond
                [(< lbs/axle 2000)  `(0.533 0)]
                [(< lbs/axle 13500) `(0.033 1.05)]
                [(< lbs/axle 20000) `(0.142 -0.42)]
                [else `(0.278 -3.115)])])
  (+ (* (first mods) (/ kips (hash-ref vehicle "axles")) (last mods))))))

(define (factor-tire vehicle)
  (/ 100 (+ 10 (hash-ref vehicle "tire-width"))))

(define (factor-grouser vehicle)
  (if (hash-has-key? vehicle "chains") 1.05 1))

(define (factor-wheel-load vehicle)
  (let ([kips (/ (hash-ref vehicle "weight") 1000)])
    (/ kips (hash-ref vehicle "wheel#"))))

(define (factor-clearance vehicle)
  (/ (hash-ref vehicle "clearance") 10))

(define (factor-transmission vehicle)
  (if (hash-has-key? vehicle "hydraulic") 1 1.05))

(define (factor-engine vehicle)
  (let ([hp/ton (/ (hash-ref vehicle "weight") 2000)])
    (if (<= hp/ton 10)  1.05 1)))  

(define (factor-contact-pressure vehicle)
  (/ (hash-ref vehicle "weight")
     (* (hash-ref vehicle "tire-width")
        (hash-ref vehicle "tire#") 
        (/ (hash-ref vehicle "tire-diameter") 2))))

(test-factors)
