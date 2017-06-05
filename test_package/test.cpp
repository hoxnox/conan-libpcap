#include <pcap.h>
#include <string.h>
#include <stdio.h>

int main(int argc, char* argv[])
{
	char errbuf[PCAP_ERRBUF_SIZE];
	errbuf[0] = 0;
	pcap_t* pcap = pcap_open_offline("test", errbuf);
	if (strlen(errbuf) > 0)
		return 0;
	return 1;
}

