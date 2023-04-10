#lang racket
#| Calculate mobility index and one pass vehicle cone index for wheeled and tracked vehicles
Sources:
  Wong, J.Y., Jayakumar, P., Toma, E., & Preston-Thomas, J. (2020).
     A review of mobility metrics for next generation vehicle mobility models.
     Journal of Terramechanics (87). 11 -20.
     https://doi.org/10.1016/j.jterra.2019.10.003.
  
  Kennedy, J.G. & Rush, E.S. (1968). Development of revised mobility index formula
     for self-propelled wheeled vehicles in fine-grained soils. 
     Trafficability of Soils. U.S. Army Materiel Command. U.S. Departmeny of the Army. 
  
  U.S. Department of the Army. (1994). Planning and design of roads, airfields,
     and heliports in the theater of operations -- airfield and heliport design:
     FM 5-430-00-1/AFPAM 32-8013, Vol 1.
     
Vehicle specs from https://en.wikipedia.org/
|#

;; use the below as a template for wheeled vehicles
(define stryker (hash "weight" 36320  ;lbs
                      "clearance" 21  ;inches
                      "axles" 4
                      "wheel#" 8
                      "tire-width" 22  ;inches
                      "hydraulic" #t
                      "tire-diameter" 45  ;inches
                      "tire#" 8
                      "hp" 350))

;; use the below as a template for tracked vehicles
(define abrams (hash "weight" 136000  ;lbs
                     "clearance" 19  ;inches
                     "length" 384.5  ;inches
                     "track-width" 25  ;inches
                     "shoe-area" 190  ;inches
                     "hydraulic" #t
                     "bogies" 7
                     "hp" 1500))


(define (test-wheeled)
  (check-equal? (wheel-factor-weight stryker) 0.314622)
  (check-equal? (exact->inexact(factor-wheel-load stryker)) 4.54)  ;github can't render fractions like Dr. Racket
  (check-equal? (wheel-factor-grouser stryker) 1)
  (check-equal? (exact->inexact (factor-tire stryker)) 3.125) 
  (check-equal? (factor-transmission stryker) 1)
  (check-equal? (factor-engine stryker) 1.05)
  (check-equal? (exact->inexact (wheel-factor-contact-pressure stryker)) 9.171717171717171)
  (check-equal? (exact->inexact (factor-clearance stryker)) 2.1)
  (check-equal? (wheel-calculate-mobility-index stryker) 3.531569664)
  (check-equal? (wheel-calculate-vci-1
                (wheel-calculate-mobility-index stryker)) 6.795455863452073))


(define (test-tracked)
  (define mi (track-calculate-mobility-index abrams))
  (displayln (format "Abrams mobility index: ~a" mi))
  (displayln (format "Abrams one-pass VCI: ~a" (track-calculate-vci-1 mi))))


(define (track-calculate-vci-1 mi)
  #|
  :param vehicle: a mobility index
  :return: the one-pass vehicle cone index for fine-grained soils
  |#
  (- (+ 7 (* 0.2 mi)) (/ 39.2 (+ mi 5.6))))


(define (wheel-calculate-vci-1 mi)
  #|
  :param vehicle: a mobility index
  :return: the one-pass vehicle cone index for fine-grained soils
  |#
  (if (< mi 115)
      (- (+ 11.48 (* 0.2 mi)) (/ 39.2 (+ mi 3.74)))
      (* 4.1 (expt mi 0.446))))


(define (wheel-calculate-mobility-index vehicle)
  #|
  :param vehicle: hash table of vehicle properties
  :return: a number reflecting the vehicle's mobility index
  |#
  (* (- (+ (/ (* (wheel-factor-contact-pressure vehicle) (wheel-factor-weight vehicle))
              (* (factor-tire vehicle) (wheel-factor-grouser vehicle)))
           (factor-wheel-load vehicle))
        (factor-clearance vehicle))
     (* (factor-engine vehicle) (factor-transmission vehicle))))


(define (track-calculate-mobility-index vehicle)
  #|
  :param vehicle: hash table of vehicle properties
  :return: a number reflecting the vehicle's mobility index
  |#
  (* (- (+ (/ (* (track-factor-contact-pressure vehicle) (track-factor-weight vehicle))
              (* (factor-track vehicle) (factor-grouser vehicle)))
           (factor-bogie vehicle))
        (factor-clearance vehicle))
     (* (factor-engine vehicle) (factor-transmission vehicle))))


(define (wheel-factor-weight vehicle)
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


(define (wheel-factor-grouser vehicle)
  (if (hash-has-key? vehicle "chains") 1.05 1))


(define (factor-wheel-load vehicle)
  (let ([kips (/ (hash-ref vehicle "weight") 1000)])
    (/ kips (hash-ref vehicle "wheel#"))))


(define (factor-clearance vehicle)
  (/ (hash-ref vehicle "clearance") 10))


(define (factor-transmission vehicle)
  (if (hash-has-key? vehicle "hydraulic") 1 1.05))


(define (factor-engine vehicle)
  (let ([hp/ton (/ (hash-ref vehicle "hp") (/ (hash-ref vehicle "weight") 2000))])
    (if (<= hp/ton 10) 1 1.05)))  

(define (wheel-factor-contact-pressure vehicle)
  (/ (hash-ref vehicle "weight")
     (* (hash-ref vehicle "tire-width")
        (hash-ref vehicle "tire#") 
        (/ (hash-ref vehicle "tire-diameter") 2))))


(define (track-factor-weight vehicle)
  (let ([wt (hash-ref vehicle "weight")])
   (cond
     [(< wt 50000)  1.0]
     [(< wt 70000)  1.2]
     [(< wt 100000) 1.4]
     [else 1.8])))


(define (factor-track vehicle)
  (/ (hash-ref vehicle "track-width") 100))


(define (factor-grouser vehicle)
  (if
   (and (hash-has-key? vehicle "grouser-ht")
        (> (hash-ref "grouser-ht") 1.5))
   1.1 1))


(define (track-factor-contact-pressure vehicle)
  (/ (hash-ref vehicle "weight")
     (* (hash-ref vehicle "length")
        (hash-ref vehicle "track-width"))))


(define (factor-bogie vehicle)
  (/
   (/ (hash-ref vehicle "weight") 10)
   (* (hash-ref vehicle "bogies") (hash-ref vehicle "shoe-area"))))

(test-wheeled)
(test-tracked)
