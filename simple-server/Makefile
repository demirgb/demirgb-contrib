host := 10.9.8.133
upload_port := 9999

FROZEN = server.mpy

all: $(FROZEN)

%.mpy: %.py
	mpy-cross -v $<

clean:
	$(RM) *.mpy

upload-all: $(patsubst %,upload-%,$(FROZEN))

upload: upload-server.mpy

upload-%: %
	(echo "RECV:$<"; cat "$<") | nc -v -N $(host) $(upload_port)

.PHONY: all clean upload upload-all

