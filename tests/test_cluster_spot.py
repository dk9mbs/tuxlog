import unittest
import config
import os
from model import model
from tuxlog.cluster import ClusterSpot
from model.model import LogDxclusterSpots

class ClusterSpotTest(unittest.TestCase):
    def test_spotparse(self):
        config.DatabaseConfig.open(model.database, config.DatabaseConfig.read_from_file(os.getenv("tuxlog_environment")))
        """
        Test that it can sum a list of integers
        """

        spot='DX de EA7FKY:     7090.0  EB7CFA       TROFEO SAN VICENTE             1625Z'

        @ClusterSpot(spot, "KHz", "MHz")
        def inner_parse(*args, **kwargs):
            #spot_type=args[0]
            json_spot=args[1]
            print(json_spot)

        inner_parse()

if __name__ == '__main__':
    unittest.main()