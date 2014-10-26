if [ -f /etc/sysconfig/ccache ]; then
    . /etc/sysconfig/ccache
fi

if [ -f /etc/sysconfig/distcc ]; then
    . /etc/sysconfig/distcc
fi

if [ "$USE_DISTCC_DEFAULT" = "yes" ]; then
  if [ "$USE_CCACHE_DEFAULT" = "yes" ]; then
      if [ -z "$CCACHE_PREFIX" ]; then
          export CCACHE_PREFIX=/usr/bin/distcc
      fi
  else
      export PATH=/usr/libexec/distcc/bin:$PATH
  fi
fi
