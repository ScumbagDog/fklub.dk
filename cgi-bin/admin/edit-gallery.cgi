#!/usr/bin/plt/bin/mzscheme -r

(define laml-dir "/usr/bin/laml/") ;  
(load (string-append laml-dir "laml.scm"))

(lib-load "cgi.scm") ;  @a
(lib-load "encode-decode.scm") ;  
(lib-load "color.scm") ;  

; HTML mirror loading
(lib-load "html4.01-transitional-validating/basis.scm")
(lib-load "html4.01-transitional-validating/surface.scm")
(lib-load "html4.01-transitional-validating/convenience.scm")

(define cgi-testing #f)

(define url-pars (extract-url-parameters))

(load "/usr/local/cgi-bin/lib/common.scm")
(cgi-lib-load "admin/admin.scm")
(cgi-lib-load "common.scm")
(cgi-lib-load "lib/file.scm")

(ensure-admin)

(define cur-gallery 
	(as-symbol (defaulted-get 'cur-gallery url-pars 'none )))
	
(define error
    (as-symbol (defaulted-get 'error url-pars 'none)))
	
(define galleries (dir-list "/data/galleries/"))

(define (get-images gallery-id) 
	(dir-list (string-append "/data/galleries/" gallery-id)))

(define gallery-overview
	(con 
		(map (lambda (g) (a 'href (string-append "edit-gallery.cgi?cur-gallery=" g) g)) galleries)
		(if (eq? error 'empty-gallery-name ) (p "Giv" (b "venligst") "galleriet et navn.") (div))
		(form-1 
			"create-gallery.cgi"
			(con 
				(text-line 'name 3 "")
				(submit "Opret")))))

(define (gallery gallery-id)
	(con
		(if (> (length (get-images gallery-id)) 0)
			(table 'border 1
				(tbody
					(map (lambda (image)
					(tr
						(td 
							(img 'width 200 'src (string-append "/galleries/" gallery-id "/" image)))
						(td 
							(form-1 
								(string-append "remove-image.cgi?cur-gallery=" gallery-id)
								(con 
									(hidden-line 'image image)
									(submit "SLET")
								)
							)))) (get-images gallery-id)))
				)
				(p "No images"))
		(multipart-form 
			(string-append "upload-images.cgi?cur-gallery=" gallery-id) 
			(string-append "/data/galleries/" gallery-id "/") 
			(string-append "/galleries/" gallery-id) 
			(con 
				(input 'type "hidden" 'name "cur-gallery" 'value gallery-id)
				(input 'type "file" 'name "images" 'multiple "")
				(submit "Tilføj billede")))
		(form-1 
			(string-append "remove-gallery.cgi?cur-gallery=" gallery-id)
			(con 
				(submit "SLET GALLERI")))))


(define page-body
	(con
		admin-menu-list
		(if (eq? 'none cur-gallery)
			gallery-overview
			(gallery (symbol->string cur-gallery)))))

(fklub-page "test" page-body)

(end)
