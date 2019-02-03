from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients


class KMSRegionConfig(RegionConfig):
    """
    KMS Configuration for a single AWS region
    """

    def parse_key(self, global_params, region, key):
        """
        Parse a single Key Management Service

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param key:                     Key
        """

        customer_master_key = {'id': key.pop('KeyId'), 'arn': key.pop('KeyArn')}

        api_client = api_clients[region]
        rotation_status = api_client.get_key_rotation_status(KeyId=customer_master_key['id'])
        customer_master_key['rotation_enabled'] = rotation_status['KeyRotationEnabled']

        self.keys[len(self.keys)] = customer_master_key


########################################
# KMSConfig
########################################

class KMSConfig(RegionalServiceConfig):
    """
    KMS configuration for all AWS regions
    """

    region_config_class = KMSRegionConfig

    def __init__(self, service_metadata, thread_config=4):
        super(KMSConfig, self).__init__(service_metadata, thread_config)
