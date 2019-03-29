(load "lib/common.scm")

(define substitutions
    '(
        (#\! . "%21")
        (#\# . "%23")
        (#\$ . "%24")
        (#\& . "%26")
        (#\' . "%27")
        (#\( . "%28")
        (#\) . "%29")
        (#\* . "%2A")
        (#\+ . "%2B")
        (#\, . "%2C")
        (#\/ . "%2F")
        (#\: . "%3A")
        (#\; . "%3B")
        (#\= . "%3D")
        (#\? . "%3F")
        (#\@ . "%40")
        (#\[ . "%5B")
        (#\] . "%5D")
        (#\space . "%20")
        (#\" . "%22")
        (#\% . "%25")
        (#\- . "%2D")
        (#\. . "%2E")
        (#\< . "%3C")
        (#\> . "%3E")
        (#\\ . "%5C")
        (#\^ . "%5E")
        (#\_ . "%5F")
        (#\` . "%60")
        (#\{ . "%7B")
        (#\| . "%7C")
        (#\} . "%7D")
        (#\~ . "%7E")
        ))

(define substitution-reversed 
    (map (lambda (x) (cons (cdr x) (car x))) substitutions))

(define (url-encode str)
    (url-encode-tail str ""))

(define (url-encode-tail str cur)
    (if (= (string-length str) 0) cur
        (let* (
            (ch (string-ref str 0))
            (res (eq-lookup ch substitutions))
            )
            (if (eq? res #f) 
                (url-encode-tail (substring str 1) (string-append cur (substring str 0 1)))
                (url-encode-tail (substring str 1) (string-append cur res))
            ))))

(define (url-decode str)
    (url-decode-tail str ""))

(define (url-decode-tail str cur)
    (if (< (string-length str) 3) 
        (string-append cur str)
        (let* (
            (substr (substring str 0 3))
            (res (eq-lookup substr substitution-reversed))
            )
            (if (eq? res #f) 
                (url-decode-tail (substring str 1) (string-append cur (substring str 0 1)))
                (url-decode-tail (substring str 3) (string-append cur (char->string res)))
            ))))
                