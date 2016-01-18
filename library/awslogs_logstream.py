#!/usr/bin/python
''' Ansible module for creating logstreams with the Cloudwatch Logs Agent '''

def main():
    ''' main() '''
    module = AnsibleModule(
        argument_spec=dict(
            datetime_format          = dict(required=True, type='str'),
            file                     = dict(required=True, type='str'),
            batch_count              = dict(type='int'),
            batch_size               = dict(type='int'),
            buffer_duration          = dict(type='int'),
            encoding                 = dict(type='str'),
            file_fingerprint_lines   = dict(type='int'),
            initial_position         = dict(choices=['start_of_file', 'end_of_file'], type='str'),
            log_group_name           = dict(type='str'),
            log_stream_name          = dict(default='{instance_id}', type='str'),
            multi_line_start_pattern = dict(type='str'),
            time_zone                = dict(choices=['LOCAL', 'UTC'], type='str'),
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

    # do nothing if contents have not changed
    if os.path.exists(logstream_fullpath) and logstream_contents == open(logstream_fullpath).read():
        module.exit_json(changed=False)
    else:
        # write contents to config file
        update_file = open(logstream_fullpath, 'w')
        update_file.write(logstream_contents)
        update_file.close()
    module.exit_json(changed=True)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
