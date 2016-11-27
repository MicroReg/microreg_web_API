'''
MicroReg Client library
Allows the python client services to connect with the Registry Server to allow
the registration and other facilities provided through Registry Server.

Made By Saurabh and Modified By Nikhil
'''


import xmlrpclib

class MicroRegClient:
    '''
    MicroRegClient defines the methods facilitating the connection with the
    MicroReg Server.
    '''

    def __init__(self,host,port):
        '''
        Setup the connection with the MicroReg server.
        '''

        self.__connection_uri = str(host).rstrip('/') + ":" + str(port)
        self.__client = xmlrpclib.ServerProxy(self.__connection_uri)

    def get_all_service_details(self):
        '''
        Get information about all the running services
        '''

        return self.__client.get_all_service_details()

    def get_reg_count(self):
        '''
        Get information count of registered services
        '''

        return self.__client.get_reg_count()


    def get_service_details(self, name):
        '''
        Get information about service
        '''

        return self.__client.get_service_details(name)

    def register(self, name, host, port):
        '''
        Register a new service
        '''

        return self.__client.register(name, host, port)

    def unregister(self, name):
        '''
        Unregister an existing service
        '''

        return self.__client.unregister(name)
