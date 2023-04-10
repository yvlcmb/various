(ns vci.mobility
  (:gen-class))

(defmulti fac-weight "calculate weight factor" 
          (fn [vehicle] (:Category vehicle)))
(defmethod fac-weight :Wheel
  [vehicle]
  (def lbs-per-axle (/ (:weight vehicle) (:axles vehicle)))
  (def kips (/ (:weight vehicle) 1000))
  (let [mods (cond
               (< lbs-per-axle 2000)  `(0.533 0)
               (< lbs-per-axle 13500) `(0.033 1.05)
               (< lbs-per-axle 20000) `(0.142 -0.42)
               :else `(0.278 -3.115))]
    (+ (* (first mods) (/ kips (:axles vehicle)) (last mods)))))
(defmethod fac-weight :Track
  [vehicle]
  (def wt (:weight vehicle))
  (cond
    (< wt 50000)  1.0
    (< wt 70000)  1.2
    (< wt 100000) 1.4
    :else 1.8))

(defn fac-tire [veh]
  "calculate the tire factor for wheeled vehicles"
  (/ 100 (+ 10 (:tire-width veh))))

(defn fac-track [veh]
  "calculate the tire factor for wheeled vehicles"
  (/ (:track-width veh) 100))

(defn fac-grouser [veh]
  "calcuate the grouser factor"
  (if (and (contains? veh :grouser-ht) (> (:veh "grouser-ht") 1.5)) 1.1 1))

(defmulti fac-pressure "calculate contact pressure factor"
  (fn [veh] (:Category veh)))
(defmethod fac-pressure :Wheel [veh]
  (/ (:weight veh) (* (:tire-width veh) (:tires veh) (/ (:tire-diameter veh) 2))))
(defmethod fac-pressure :Track [veh]
  (/ (:weight veh) (* (:length veh) (:track-width veh))))

(defn fac-bogie [veh]
  "calculate the bogie factor for tracked vehicles"
  (/ (/ (:weight veh) 10) (* (:bogies veh) (:shoe-area veh))))

(defn fac-engine [veh]
  "calculate the engine factor"
  (let [hp-per-ton (/ (:hp veh) (/ (:weight veh) 2000))]
    (if (<= hp-per-ton 10) 1 1.05)))

(defn fac-transmission [veh]
  "calculate the tranmission factor"
  (if (contains? veh :hydraulic) 1 1.05))

(defn fac-clearance [veh]
  "calculate the clearance factor"
  (/ (:clearance veh) 10))

(defn fac-wheel-load [veh]
  "calculate the wheel load factor for wheeled vehicles"
  (/ (/ (:weight veh) 1000) (:wheels veh)))

(defmulti calculate-mobility-index "calculate mobility index"
  (fn [veh] (:Category veh)))
(defmethod calculate-mobility-index :Wheel [veh]
  (* (- (+ (/ (* (fac-pressure veh) (fac-weight veh))
              (* (fac-tire veh) (fac-grouser veh)))
           (fac-wheel-load veh))
        (fac-clearance veh))
     (* (fac-engine veh) (fac-transmission veh))))
(defmethod calculate-mobility-index :Track [veh]
  (* (- (+ (/ (* (fac-pressure veh) (fac-weight veh))
              (* (fac-track veh) (fac-grouser veh)))
           (fac-bogie veh))
        (fac-clearance veh))
     (* (fac-engine veh) (fac-transmission veh))))

(defn calculate-vci1-track [mi]
  "return the one-pass wheeled vehicle cone index for fine-grained soils"
  (- (+ 7 (* 0.2 mi)) (/ 39.2 (+ mi 5.6))))

(defn calculate-vci1-wheel [mi]
  "return the one-pass tracked vehicle cone index for fine-grained soils"
  (if (< mi 115)
    (- (+ 11.48 (* 0.2 mi)) (/ 39.2 (+ mi 3.74)))
    (* 4.1 (Math/pow mi 0.446))))

(defn main []
  (def stryker {:Category :Wheel
                :weight 36320
                :axles 4
                :clearance 21
                :wheels 8
                :tire-width 22
                :hydraulic true
                :tire-diameter 45
                :tires 8
                :hp 350})

  (def abrams {:Category :Track
               :weight 136500
               :clearance 19
               :length 384.5
               :track-width 25
               :shoe-area 190
               :hydraulic true
               :bogies 7
               :hp 1500})

  (println (calculate-vci1-wheel (calculate-mobility-index stryker)))
  (println (calculate-vci1-track (calculate-mobility-index abrams))))

(main)
