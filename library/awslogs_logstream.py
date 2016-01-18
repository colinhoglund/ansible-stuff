#!/usr/bin/python
''' Ansible module that creates logstreams for the Cloudwatch Logs Agent '''

#TODO: get output to work with --diff flag

DOCUMENTATION = '''
---
module: awslogs_logstream
author:
    - Colin Hoglund (@colinhoglund)
short_description: Creates logstreams for the Cloudwatch Logs Agent
description:
  - This module assumes you already have the Cloudwatch Logs Agent already installed
    Each logstream is stored in a separate file in the /var/awslogs/etc/config/ directory.
    (U(http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CWL_GettingStarted.html)).
notes:
  - This module supports check mode.
options:
  batch_count:
    required: false
    default: 1000
    description:
      - Specifies the max number of log events in a batch, up to 10000.
  batch_size:
    required: false
    default: 32768
    description:
      - Specifies the max size of log events in a batch, in bytes, up to 1048576 bytes.
        This size is calculated as the sum of all event messages in UTF-8,
        plus 26 bytes for each log event.
  buffer_duration:
    required: false
    default: 5000
    description:
      - Specifies the time duration for the batching of log events. The minimum value is 5000ms.
  datetime_format:
    required: true
    description:
      - Specifies how the timestamp is extracted from logs.
  encoding:
    required: false
    default: 'utf_8'
    description:
      - Specifies the encoding of the log file so that the file can be read correctly.
  file:
    aliases: ['name']
    required: true
    description:
      - Specifies log files that you want to push to CloudWatch Logs.
  file_fingerprint_lines:
    required: false
    default: '1'
    description:
      - Specifies the range of lines for identifying a file. The valid values are one
        number or two dash delimited numbers, such as '1', '2-5'.
  initial_position:
    choices: ["start_of_file", "end_of_file"]
    required: false
    default: 'start_of_file'
    description:
      - Specifies where to start to read data.
  log_group_name:
    required: false
    description:
      - Specifies the destination log group. The default value is the value of the file argument.
  log_stream_name:
    required: false
    default: '{instance_id}'
    description:
      - Specifies the destination log stream. You can use a literal string or
        predefined variables ({instance_id}, {hostname}, {ip_address}), or
        combination of both to define a log stream name.
  multi_line_start_pattern:
    required: false
    default: '^[^\s]'
    description:
      - Specifies the pattern for identifying the start of a log message.
  time_zone:
    choices: ["LOCAL", "UTC"]
    required: false
    default: 'LOCAL'
    description:
      - Specifies the time zone of log event timestamp.
'''

EXAMPLES = '''
- name: Create nginx access logstream
  awslogs_logstream:
    file: /var/log/nginx/access.log*
    datetime_format: '%d/%b/%Y:%H:%M:%S'

- name: Create standard Ubuntu logstreams
  awslogs_logstream:
    file: "{{item}}"
    datetime_format: '%b %d %H:%M:%S'
  with_items:
    - /var/log/syslog
    - /var/log/auth.log
'''

def main():
    ''' main() '''
    module = AnsibleModule(
        argument_spec=dict(
            datetime_format          = dict(required=True, type='str'),
            file                     = dict(required=True, type='str'),
            batch_count              = dict(required=False, type='int'),
            batch_size               = dict(required=False, type='int'),
            buffer_duration          = dict(required=False, type='int'),
            encoding                 = dict(required=False, type='str'),
            file_fingerprint_lines   = dict(required=False, type='int'),
            initial_position         = dict(choices=['start_of_file', 'end_of_file'],
                                            required=False, type='str'),
            log_group_name           = dict(required=False, type='str'),
            log_stream_name          = dict(default='{instance_id}', required=False, type='str'),
            multi_line_start_pattern = dict(required=False, type='str'),
            time_zone                = dict(choices=['LOCAL', 'UTC'], required=False, type='str'),
        ),
        supports_check_mode=True
    )

    # file vars
    logstream_config_dir = '/var/awslogs/etc/config/'
    logstream_filename = module.params['file'].replace('/', '_')
    logstream_fullpath = logstream_config_dir+logstream_filename

    # log_group_name is required by agent, default to value of file
    if not module.params['log_group_name']:
        module.params['log_group_name'] = module.params['file']

    # build logstream config file
    logstream_contents = '[{}]\n'.format(module.params['file'])
    for arg in module.params.items():
        if arg[1] and not arg[0].startswith('_ansible'):
            logstream_contents += '{} = {}\n'.format(arg[0], arg[1])

    # the cloudwatch logs agent should be installed before calling this module
    if not os.path.exists(logstream_config_dir):
        module.fail_json(
            msg='{} does not exist, awslogs may not be installed'.format(logstream_config_dir)
        )

    # no changes if contents have not changed
    if os.path.exists(logstream_fullpath) and logstream_contents == open(logstream_fullpath).read():
        module.exit_json(path=logstream_fullpath, changed=False)
    # no changes if check_mode enabled
    elif not module.check_mode:
        # write contents to config file
        update_file = open(logstream_fullpath, 'w')
        update_file.write(logstream_contents)
        update_file.close()
    module.exit_json(path=logstream_fullpath, changed=True)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
