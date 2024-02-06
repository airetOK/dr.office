CREATE TABLE IF NOT EXISTS public."patients"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "fullName" character varying(80) COLLATE pg_catalog."default" NOT NULL,
    teeth character varying(100) COLLATE pg_catalog."default",
    actions character varying(500) COLLATE pg_catalog."default",
    price character varying(30) COLLATE pg_catalog."default",
    date date NOT NULL,
    CONSTRAINT "Patients_pkey" PRIMARY KEY (id)
)