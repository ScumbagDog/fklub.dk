#!/usr/bin/plt/bin/mzscheme -r

(define laml-dir "/usr/bin/laml/") ;  
(load (string-append laml-dir "laml.scm"))

(lib-load "cgi.scm") ;  @a
(lib-load "encode-decode.scm") ;  

; HTML mirror loading
(lib-load "html4.01-transitional-validating/basis.scm")
(lib-load "html4.01-transitional-validating/surface.scm")
(lib-load "html4.01-transitional-validating/convenience.scm")

(define cgi-testing #f)

(load "/usr/local/cgi-bin/lib/common.scm")
(cgi-lib-load "admin/admin.scm")
(cgi-lib-load "common.scm")
(cgi-lib-load "lib/file.scm")

(ensure-admin)

(define questions 
	(let ((data (safe-read "/data/faq.scm" '()))) 
		(if (list? data) (reverse data) (list))))

(define (faq questions) 
	  	(container 
			(h3 "Spørgsmål")
		    (if (null? questions) (p "Ingen spørgsmål")
				(table 'border 1
					(thead
						(tr
							(th "Spørgsmål")
							(th "Svar")
							(th "Slet")))
					(tbody 
						(map (lambda (x) 
							(tr 
								(td (car x))
								(td (cdr x))
								(td 
									(form-1
										"remove-faq.cgi"
										(con
											(hidden-line 'question (car x))
											(submit "SLET")))
								))) questions)))
				)
			(h3 "Tilføj nyt spørgsmål")
		 	(form-1 
		 		"upload-faq.cgi"
		 		(con 
					(label 'for 'question "Spørgsmål")
		 			(input-text 'question "Spørgsmål")
					(br)
					(label 'for 'answer "Svar")
		 			(input-text 'answer "Svar")
					(br)
		 			(submit-btn "Tilføj FAQ")
		 		)
		 	)))

(fklub-page "Rediger FAQ" (con admin-menu-list (faq questions)))

(end)
