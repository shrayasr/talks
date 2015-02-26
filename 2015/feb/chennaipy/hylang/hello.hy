(defn say_hello 
  [name]
  (print (+ "Hello " name)))

(if (= __name__ "__main__")
  (do
    (setv whom (raw-input))
    (say_hello whom)))
