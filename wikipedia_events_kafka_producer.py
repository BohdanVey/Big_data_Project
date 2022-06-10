import json
import argparse
from sseclient import SSEClient as EventSource
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
def create_kafka_producer(bootstrap_server):
    try:
        producer = KafkaProducer(bootstrap_servers=bootstrap_server,
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    except NoBrokersAvailable:
        print('No broker found at {}'.format(bootstrap_server))
        raise
    
    
    if producer.bootstrap_connected():
        print('Kafka producer connected!')
        return producer
    else:
        print('Failed to establish connection!')
        exit(1)



def init_namespaces():
    # create a dictionary for the various known namespaces
    # more info https://en.wikipedia.org/wiki/Wikipedia:Namespace#Programming
    namespace_dict = {-2: 'Media',
                      -1: 'Special',
                      0: 'main namespace',
                      1: 'Talk',
                      2: 'User', 3: 'User Talk',
                      4: 'Wikipedia', 5: 'Wikipedia Talk',
                      6: 'File', 7: 'File Talk',
                      8: 'MediaWiki', 9: 'MediaWiki Talk',
                      10: 'Template', 11: 'Template Talk',
                      12: 'Help', 13: 'Help Talk',
                      14: 'Category', 15: 'Category Talk',
                      100: 'Portal', 101: 'Portal Talk',
                      108: 'Book', 109: 'Book Talk',
                      118: 'Draft', 119: 'Draft Talk',
                      446: 'Education Program', 447: 'Education Program Talk',
                      710: 'TimedText', 711: 'TimedText Talk',
                      828: 'Module', 829: 'Module Talk',
                      2300: 'Gadget', 2301: 'Gadget Talk',
                      2302: 'Gadget definition', 2303: 'Gadget definition Talk'}

    return namespace_dict


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='EventStreams Kafka producer')

    parser.add_argument('--bootstrap_server', default='localhost:9092', help='Kafka bootstrap broker(s) (host[:port])', type=str)
    parser.add_argument('--topic_name', default='wikipedia-events', help='Destination topic name', type=str)
    parser.add_argument('--events_to_produce', help='Kill producer after n events have been produced', type=int, default=1000)

    return parser.parse_args()


if __name__ == "__main__":
    # parse command line arguments
    args = parse_command_line_arguments()

    # init producer
    producer = create_kafka_producer(args.bootstrap_server)

    # init dictionary of namespaces
    namespace_dict = init_namespaces()

    # used to parse user type
    user_types = {True: 'bot', False: 'human'}

    # consume websocket
    url = 'https://stream.wikimedia.org/v2/stream/page-create'
    
    print('Messages are being published to Kafka topic')
    messages_count = 0
    
    for event in EventSource(url):
        if event.event == 'message':
            try:
                event_data = json.loads(event.data)
                print(event_data)
            except ValueError:
                pass
        if messages_count >= args.events_to_produce:
            print('Producer will be killed as {} events were producted'.format(args.events_to_produce))
            exit(0)