def osdetect(buildout):
    import sys
    import platform
    import os

    platforms = ['default']
    if sys.platform == 'darwin':
        platforms.insert(0, 'darwin')
        mac_ver = platform.mac_ver()
        if mac_ver[0].startswith('10.5'):
            platforms.insert(0, 'darwin-leopard')
        elif mac_ver[0].startswith('10.6'):
            platforms.insert(0, 'darwin-snowleopard')
            if sys.maxint > 2147483647:
                platforms.insert(0, 'darwin-snowleopard-64')
        elif mac_ver[0].startswith('10.7'):
            platforms.insert(0, 'darwin-lion')
        elif mac_ver[0].startswith('10.8'):
            platforms.insert(0, 'darwin-mountainlion')
    elif sys.platform == 'linux2':
        dist, version, name = platform.dist()
        dist = dist.lower()
        platforms.insert(0, '-'.join([sys.platform, dist]))
        if name:
            name = name.lower()
            platforms.insert(0, '-'.join([sys.platform, dist, name]))

        if dist == 'debian':
            # In Debian the name always return an empty string.
            name = 'unknown'
            # In testing and unstable the distribution code name is returned
            # in the version field, as:
            # '<testing codename>/<unstable codename>'; ex: 'jessie/sid'.
            testing = 'jessie'
            if testing in version:
                name = testing
            # When a new relese is made, the testing code name change, but the
            # unstable don't, so the 'sid' name is going to be in the version.
            elif 'sid' in version:
                name = 'sid'
            else:
                try:
                    version = float(version)
                except ValueError:
                    # This no't should happer never, because when testing is
                    # relased as the stable distribution, it start o use the
                    # version number.
                    pass
                else:
                    # Older versions works with out need of patches, at least
                    # for now.
                    if 7 <= version < 8:
                        name = 'wheezy'
                    elif 8 <= version < 9:
                        name = 'jessie'

            platforms.insert(0, '-'.join([sys.platform, dist, name]))
        else:
            platforms.insert(0, '-'.join([sys.platform, dist, version]))

    elif platform.machine() == 'x86_64':
        platforms.insert(0, 'x86_64')

    if os.path.exists('/usr/lib/i386-linux-gnu'):
        platforms.insert(0, 'i386-linux-gnu')

    buildout._logger.debug("Detected these platforms: %s" % ", ".join(platforms))

    variants = {}
    parts = set()
    for key in buildout.keys():
        if ':' not in key:
            continue
        part, variant = key.split(':')
        variants.setdefault(variant, []).append((part, key))
        parts.add(part)

    for platform in platforms:
        for part, key in variants.get(platform, []):
            if part in buildout._raw:
                continue
            buildout._raw[part] = buildout._raw[key].copy()
