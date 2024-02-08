DROP TABLE IF EXISTS public."patients";
CREATE TABLE public."patients"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    "fullName" character varying(80) COLLATE pg_catalog."default" NOT NULL,
    teeth character varying(100) COLLATE pg_catalog."default",
    actions character varying(500) COLLATE pg_catalog."default",
    price character varying(30) COLLATE pg_catalog."default",
    date date NOT NULL,
    CONSTRAINT "Patients_pkey" PRIMARY KEY (id)
);

INSERT INTO public."patients"(
	"fullName", teeth, actions, price, date)
	VALUES ('Безрукавий Сергій', '16,17', 'реставрація, консультація', '100.50', '2024-02-05');
INSERT INTO public."patients"(
	"fullName", teeth, actions, price, date)
	VALUES ('Пригара Іван', '46', 'ендо', '150', '2024-02-06');
INSERT INTO public."patients"(
	"fullName", teeth, actions, price, date)
	VALUES ('Шевцов Богдан', '', 'чистка', '70', '2024-02-06');
INSERT INTO public."patients"(
	"fullName", teeth, actions, price, date)
	VALUES ('Микита Валерія', '21,22', 'реставрація', '180', '2024-02-11');
INSERT INTO public."patients"(
	"fullName", teeth, actions, price, date)
	VALUES ('Шетеля Володимир', '23', 'ендо', '120', '2024-02-11');
INSERT INTO public."patients"(
	"fullName", teeth, actions, price, date)
	VALUES ('Форос Анатолій', '34', 'ендо', '150', '2024-02-12');