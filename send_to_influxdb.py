from influxdb import InfluxDBClient


def send_data_to_influxDB(
    host, port, un, pw, db, data, measurement, field_attributes, tag_attributes
):
    # pushes data to InfluxDB
    # measurement is a measurement in influxdb
    # field_attributes is a list of attributes that will be sent as fields
    # tag_attribues is a list of attributes that will be sent as tags
    # data is a dict with keys being field and tag attributes, as well as key time with time of the measurement in UTC
    client = InfluxDBClient(host=host, port=port, username=un, password=pw)
    client.switch_database(db)
    tags = {}
    if tag_attributes:
        for key in tag_attributes:
            tags.update({key: data[key]})
    fields = {}
    for field in field_attributes:
        fields.update({field: float(data[field])})
    json_body = [
        {
            "measurement": measurement,
            "tags": tags,
            "time": data["time"],
            "fields": fields,
        }
    ]
    return client.write_points(json_body)
