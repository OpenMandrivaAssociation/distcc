if ( -f /etc/sysconfig/ccache ) then
    eval `sed -n 's/^\([^#]*\)=\([^#]*\)/set \1=\2;/p' < /etc/sysconfig/ccache`
endif

if ( -f /etc/sysconfig/distcc ) then
    eval `sed -n 's/^\([^#]*\)=\([^#]*\)/set \1=\2;/p' < /etc/sysconfig/distcc`
endif

if ($?USE_DISTCC_DEFAULT) then
  if ( "$USE_DISTCC_DEFAULT" == "yes" ) then
    if ($?USE_CCACHE_DEFAULT) then

  if ( "$USE_CCACHE_DEFAULT" == "yes" ) then
      if ( "$path" !~ */usr/libexec/distcc/bin* ) then
          setenv CCACHE_PREFIX /usr/bin/distcc
      endif
  else
      set path = ( /usr/libexec/distcc/bin $path )
  endif
    else
      set path = ( /usr/libexec/distcc/bin $path)
    endif
  endif
endif
